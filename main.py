"""
The file which runs the web application
"""

# Standard Library Imports
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, UTC
import asyncio
import json

# Local Imports
from app.models import AgentRequest, AgentResponse, StartGameResponse, StartGameRequest, AddTimeRequest, AddMessagesRequest
from app.agents.triage_agent import run_agent
from app.database import add_new_user, get_cosmos_db, update_user_time, update_user_messages, update_message_timeout
from app.timeout_manager import timeout_watchdog

# Third Party Imports
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
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
        # Run agent
        response = await run_agent(body.message, body.conversation_id)
        
        # Update DB
        update_message_timeout(body.conversation_id, datetime.now(UTC).isoformat(), "agent", response.final_output)
        
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
