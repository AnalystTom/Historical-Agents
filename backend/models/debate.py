from backend.models.common import GameState, HistoricalFigure
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class PlayerType(str, Enum):
    CPU = "cpu"
    USER = "user"

class DebateConfig(BaseModel):
    topic: str
    location: str
    player1_type: PlayerType
    player2_type: PlayerType
    figure1: HistoricalFigure
    figure2: HistoricalFigure
    max_turns: int = 5

class DebateState(GameState):
    config: DebateConfig
    current_turn: int = 0
    turns: List[str] = []
    status: str = "active"