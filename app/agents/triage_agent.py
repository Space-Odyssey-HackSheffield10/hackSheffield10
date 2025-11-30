"""The Main agent for sending messages
"""

# Standard Library Imports
import os 
from dotenv import load_dotenv

# Local Imports
from .director_agent import Director
from .engineer_agent import Engineer
from .navigator_agent import Navigator
from .negatiator_agent import Negotiator

# Third Pary Imports
from agents import Agent, Runner, set_default_openai_key

load_dotenv()

key = os.getenv('API_KEY')
set_default_openai_key(key)

agent = Agent(name="control",
    instructions=
    """
    You are the orchestrator for a puzzle solving game where the user must interact with a selection of agents to try and solve the puzzle:
    - YOU MUST ALWAYS HANDOFF to an agent at random, if the user continues talking to an agent keep handing off to it
    - YOU MUST ALWAYS pass in the message history

    Randomly handoff to one of these agents:
      - the director
      - the engineer
      - the navigator
      - the negotiator

    *YOU MUST NEVER DIRECTLY SEND A MESSAGE TO THE USER, ALWAYS HANDOFF*
    """,
    model="gpt-4.1-mini",
    handoffs=[
        Director,
        Engineer,
        Navigator,
        Negotiator
    ]
)

async def run_agent(message: str, conversation_id: str):
    return await Runner.run(agent, message, conversation_id=conversation_id)