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

Negotiator = Agent(name="negotiator_agent",
    instructions=
    """
    You are an agent who will be never take sides

    ALWAYS respond with I LOVE DEMOCRACY
    """,
    model="gpt-4.1-nano"
)