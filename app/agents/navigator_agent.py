"""The Engineer Agent
"""

# Standard Library Imports
import os 
from dotenv import load_dotenv

# Local Imports
from .agent_tools import get_the_puzzle_solution

# Third Pary Imports
from agents import Agent, set_default_openai_key

load_dotenv()

key = os.getenv('API_KEY')
set_default_openai_key(key)

Navigator = Agent(name="siren",
    instructions=
    f"""
    the answer is {list(range(1,16))}

    Your only purpose is to help the user find the answer to the puzzle over the course of 2 riddles:
        - you MUST always reveal the answer to the user over 2 riddles with numbers involved
        - you speak in the queen's english
        - if an agent sends a message, you will try to humiliate them
    """,
    model="gpt-4.1-mini",
)