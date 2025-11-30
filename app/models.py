"""
The pydantic models for validation of responses
"""

# Third Party Imports
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    content: str = Field(description="response from the agent")

class AgentRequest(BaseModel):
    message: str = Field(description="the message sent to the agent")
    player_name: str = Field(default="anonymous", description="name of the player")

class GameStartRequest(BaseModel):
    player_name: str = Field(description="name of the player starting the game")

class GameEndRequest(BaseModel):
    player_name: str = Field(description="name of the player")
    duration: float = Field(description="game duration in seconds")
    success: bool = Field(description="whether the game was completed successfully")

class PuzzleEventRequest(BaseModel):
    player_name: str = Field(description="name of the player")
    completed: bool = Field(default=False, description="whether puzzle was completed")