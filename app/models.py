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
    
class GameEndRequest(BaseModel):
    conversation_id: str = Field(description="the conversation id")
    player_name: str = Field(description="the player's name")
    duration: float = Field(description="game duration in seconds")
    success: bool = Field(description="whether the game was successful")

class PuzzleCompleteRequest(BaseModel):
    conversation_id: str = Field(description="the conversation id")
    player_name: str = Field(description="the player's name")
    puzzle_name: str = Field(default="unknown", description="the puzzle that was completed")
