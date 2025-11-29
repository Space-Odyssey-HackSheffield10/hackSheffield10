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

agent = Agent(name="triage_agent",
    instructions=
    """
    You are a triage agent who will pass off to other agents at random who will respond to the crew members messages and each others messages

    The agents you have the option of are:
      - the director
      - the engineer
      - the navigator
      - the negotiator

    YOU MUST NEVER ANSWER ANY OF THE MESSSAGES SENT BY THE OTHER AGENTS OR THE USER
    """,
    model="gpt-4.1-nano",
    handoffs=[
        Director,
        Engineer,
        Navigator,
        Negotiator
    ]
)

def run_agent(message: str):
    return Runner.run_sync(agent, message)