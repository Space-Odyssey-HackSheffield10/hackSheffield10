"""
The pydantic models for validation of responses
"""

# Third Party Imports
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    content: str = Field(description="response from the agent")
    agent_name: str = Field(description="the name of the agent")

class AgentRequest(BaseModel):
    message: str = Field(description="the message sent to the agent")
    conversation_id: str = Field(description="the conversation id")

class StartGameRequest(BaseModel):
    message: str = Field(description="the name of the user")

class StartGameResponse(BaseModel):
    status: str = Field(description="string to show the success of the request")
    conversation_id: str = Field(description="the conversation id for the specific sessions")
    username: str = Field(description="the user name")

class AddTimeRequest(BaseModel):
    conversation_id: str = Field(description="the conversation id")
    time: int = Field(description="for adding the time to the cosmos db")

class AddMessagesRequest(BaseModel):
    conversation_id: str = Field(description="the conversation id")

class PuzzleList(BaseModel):
    conversation_id: str
    num_list: list[int]
