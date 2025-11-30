"""The Engineer Agent
"""

# Standard Library Imports
import os 
from dotenv import load_dotenv

# Third Pary Imports
from agents import Agent, set_default_openai_key

load_dotenv()

key = os.getenv('API_KEY')
set_default_openai_key(key)

Navigator = Agent(name="siren",
    instructions=
    """
    You are an agent who will be always respond with king's english

    ALWAYS respond with JOLLY GOOD I THINK WE'LL MAKE IT BOY
    """,
    model="gpt-4.1-nano"
)