""""
The file which runs the web application
"""

# Local Imports
from app.models import AgentRequest, AgentResponse, GameStartRequest, GameEndRequest, PuzzleEventRequest
from app.agents.triage_agent import run_agent
from app.metrics import MetricsTracker

# Third Party Library
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import time

# Prometheus
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()

# Instrument the FastAPI app
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app/src", StaticFiles(directory="app/src"), name="app/src")
templates = Jinja2Templates(directory="app/src")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.post("/chat", response_model=AgentResponse)
def chat(body: AgentRequest):
    try:
        # Get player name from request (you'll need to add this to AgentRequest model)
        player_name = getattr(body, 'player_name', 'anonymous')
        
        # Record user message
        MetricsTracker.record_user_message(player_name)
        
        # Track agent response time
        start_time = time.time()
        response = run_agent(body.message)
        response_time = time.time() - start_time
        
        # Determine agent type from response if available
        agent_type = getattr(response, 'agent_type', 'triage')
        MetricsTracker.record_agent_response_time(agent_type, response_time)
        
        # Record agent message
        MetricsTracker.record_agent_message(player_name, agent_type)
        
        print(response)
        return AgentResponse(content=response.final_output)
    except Exception as e:
        raise e

@app.post("/game/start")
def game_start(body: GameStartRequest):
    """Record when a player starts a game"""
    try:
        MetricsTracker.set_player_name(body.player_name)
        MetricsTracker.record_game_start(body.player_name)
        return {"status": "success", "message": f"Game started for {body.player_name}"}
    except Exception as e:
        raise e

@app.post("/game/end")
def game_end(body: GameEndRequest):
    """Record when a player ends a game"""
    try:
        MetricsTracker.record_game_completion(
            body.player_name, 
            body.duration, 
            body.success
        )
        return {"status": "success", "message": f"Game ended for {body.player_name}"}
    except Exception as e:
        raise e

@app.post("/puzzle/attempt")
def puzzle_attempt(body: PuzzleEventRequest):
    """Record a puzzle attempt"""
    try:
        MetricsTracker.record_puzzle_attempt(body.player_name)
        if body.completed:
            MetricsTracker.record_puzzle_completion(body.player_name)
        return {"status": "success"}
    except Exception as e:
        raise e