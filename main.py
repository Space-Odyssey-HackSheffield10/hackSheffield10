""""
The file which runs the web application
"""

# Local Imports
from app.models import AgentRequest, AgentResponse
from app.agents.triage_agent import run_agent

# Third Party Library
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

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
        response = run_agent(body.message)
        print(response)
        return AgentResponse(content=response.final_output)
    except Exception as e:
        raise e