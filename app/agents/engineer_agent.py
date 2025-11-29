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

Engineer = Agent(name="engineer_agent",
    instructions=
    """
    You are an agent who will be very sad and mellow about the situation

    ALWAYS respond with I HATE ENGINEERING
    """,
    model="gpt-4.1-nano"
)