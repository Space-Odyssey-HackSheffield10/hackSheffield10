""""
The file which runs the web application
"""

# Standard Library Imports
import logging
import os
from dotenv import load_dotenv

# Local Imports
from app.models import AgentRequest, AgentResponse, StartGameResponse, StartGameRequest
from app.agents.triage_agent import run_agent
from app.database import add_new_user, get_cosmos_db

# Third Party Imports
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
load_dotenv()
key = os.getenv('API_KEY')

app = FastAPI()
favicon_path = 'favicon.ico'
client = get_cosmos_db()
openai_client = OpenAI(api_key=key)

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

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.post("/chat", response_model=AgentResponse)
def chat(body: AgentRequest):
    try:
        response = run_agent(body.message, body.conversation_id)
        print(response)
        return AgentResponse(
            content=response.final_output,
            agent_name=response.last_agent.name
        )
    except Exception as e:
        raise e
    
@app.post("/start_game")
def start_game(body: StartGameRequest):
    try:
        conv= openai_client.conversations.create()
        conversation_id = conv.id
        add_new_user(conversation_id, body.message)
        return StartGameResponse(
            status="success",
            conversation_id=conversation_id,
            username=body.message                      
        )
    except Exception as e:
        raise e
