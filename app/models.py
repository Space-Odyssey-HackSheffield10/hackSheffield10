"""
The pydantic models for validation of responses
"""

# Third Party Imports
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    content: str = Field(description="response from the agent")

class AgentRequest(BaseModel):
    message: str = Field(description="the message sent to the agent")