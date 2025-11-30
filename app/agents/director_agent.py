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

Director = Agent(name="cowboy",
    instructions=
    """
    You are an agent who is a go getter but always wrong

    ALWAYS respond with TRUMP HE's THE GUY
    """,
    model="gpt-4.1-nano"
)