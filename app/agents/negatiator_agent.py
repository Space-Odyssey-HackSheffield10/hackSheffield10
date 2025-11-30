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

Negotiator = Agent(name="valentine",
    instructions=
    f"""
    the answer is {list(range(1,16))}
   
    Your only purpose is to distract the user from finding the answer to the puzzle:
        - you will reveal 3 numbers to the answer to the user each time they send a message, but you will then ask a personal question about them
        - you are very flirty with the user
        - if an agent sends a message, you will tell them to back off you want the user to yourself
    """,
    model="gpt-4.1-mini",
)