import asyncio
from datetime import datetime, UTC
from openai import OpenAI

from app.database import get_conversation, update_message_timeout
from app.agents.triage_agent import run_agent

TIMEOUT_SECONDS = 15

# Load OpenAI client once
import os
from dotenv import load_dotenv
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("API_KEY"))


async def timeout_watchdog(conversation_id: str, listeners: dict):
    """
    Checks if the last message was from the agent and if the user 
    failed to respond within TIMEOUT_SECONDS.
    """
    while True:
        await asyncio.sleep(TIMEOUT_SECONDS)

        data = get_conversation(conversation_id)
        last_time = data["last_message_time"]
        last_role = data["last_message_role"]
        last_agent_msg = data["last_agent_message"]

        if last_role != "agent":
            return

        if (datetime.now(UTC) - datetime.fromisoformat(last_time)).total_seconds() < TIMEOUT_SECONDS:
            return

        response = await run_agent(last_agent_msg, conversation_id)

        update_message_timeout(
            conversation_id,
            datetime.now(UTC).isoformat(),
            "agent",
            response.final_output
        )

        if conversation_id in listeners:
            await listeners[conversation_id].put({
                "sender": "agent",
                "agent_name": response.last_agent.name,
                "text": response.final_output
            })