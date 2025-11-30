"""
The file which runs the web application
"""

# Standard Library Imports
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import json

# Local Imports
from app.models import AgentRequest, AgentResponse, StartGameResponse, StartGameRequest, AddTimeRequest, AddMessagesRequest
from app.agents.triage_agent import run_agent
from app.database import add_new_user, get_cosmos_db, update_user_time, update_user_messages, update_message_timeout, get_all_users, get_conversation
from app.timeout_manager import timeout_watchdog
from app.metrics import MetricsTracker

# Third Party Imports
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import time

# Prometheus
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.responses import FileResponse, StreamingResponse
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
load_dotenv()
key = os.getenv('API_KEY')

# Shared listener queues
listeners = {}

app = FastAPI()
favicon_path = 'favicon.ico'
client = get_cosmos_db()
openai_client = OpenAI(api_key=key)

# Instrument the FastAPI app
Instrumentator().instrument(app).expose(app)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
app.mount("/app/src", StaticFiles(directory="app/src"), name="app/src")
templates = Jinja2Templates(directory="app/src")

# -------------------- ROUTES --------------------

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

# -------------------- CHAT --------------------
@app.post("/chat", response_model=AgentResponse)
async def chat(body: AgentRequest, background_tasks: BackgroundTasks):
    try:
        # Get player name from conversation
        player_name = 'anonymous'
        try:
            conv_data = await asyncio.to_thread(get_conversation, body.conversation_id)
            player_name = conv_data.get('name', 'anonymous')
        except:
            pass
        
        # Record user message
        MetricsTracker.record_user_message(player_name)
        
        # Track agent response time
        start_time = time.time()
        response = await run_agent(body.message, body.conversation_id)
        response_time = time.time() - start_time
        
        # Determine agent type from response
        agent_type = getattr(response.last_agent, 'name', 'triage') if hasattr(response, 'last_agent') else 'triage'
        MetricsTracker.record_agent_response_time(agent_type, response_time)
        
        # Record agent message
        MetricsTracker.record_agent_message(player_name, agent_type)
        
        # Update DB
        update_message_timeout(body.conversation_id, datetime.now(datetime.UTC).isoformat(), "agent", response.final_output)
        
        # Start watchdog
        background_tasks.add_task(timeout_watchdog, body.conversation_id, listeners)
        
        # Push message to frontend if SSE is active
        if body.conversation_id in listeners:
            await listeners[body.conversation_id].put({
                "sender": "agent",
                "agent_name": response.last_agent.name,
                "text": response.final_output
            })
        
        return AgentResponse(
            content=response.final_output,
            agent_name=response.last_agent.name
        )
    except Exception as e:
        raise e

# -------------------- START GAME --------------------
@app.post("/start_game")
def start_game(body: StartGameRequest):
    try:
        conv = openai_client.conversations.create()
        conversation_id = conv.id
        add_new_user(conversation_id, body.message)
        return StartGameResponse(
            status="success",
            conversation_id=conversation_id,
            username=body.message
        )
    except Exception as e:
        raise e

# -------------------- ADD TIME / MESSAGES --------------------
@app.post("/add_time")
def add_time(body: AddTimeRequest):
    try:
        update_user_time(body.conversation_id, body.time)
    except Exception as e:
        raise e

@app.post("/add_messages")
def add_messages(body: AddMessagesRequest):
    try:
        conv = openai_client.conversations.items.list(body.conversation_id)
        messages = len(conv.data)
        update_user_messages(body.conversation_id, messages)
    except Exception as e:
        raise e

# -------------------- SSE EVENTS --------------------
@app.get("/events/{conversation_id}")
async def sse_events(conversation_id: str):
    queue = asyncio.Queue()
    listeners[conversation_id] = queue

    async def event_stream():
        try:
            while True:
                msg = await queue.get()
                yield f"data: {json.dumps(msg)}\n\n"
        except asyncio.CancelledError:
            # Client disconnected, remove listener
            listeners.pop(conversation_id, None)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# -------------------- BACKGROUND TASKS --------------------
async def update_metrics_from_db():
    """Background task to periodically update Prometheus metrics from Cosmos DB"""
    while True:
        try:
            # Fetch all users from Cosmos DB
            users = await asyncio.to_thread(get_all_users)
            
            # Update metrics
            MetricsTracker.update_from_cosmos_db(users)
            
            LOGGER.info(f"Updated metrics for {len(users)} users from Cosmos DB")
        except Exception as e:
            LOGGER.error(f"Error updating metrics from Cosmos DB: {e}")
        
        # Wait 10 seconds before next update
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    LOGGER.info("Starting background metrics update task")
    asyncio.create_task(update_metrics_from_db())
