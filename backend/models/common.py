from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class HistoricalFigure(BaseModel):
    name: str
    era: str
    expertise: List[str]

class GameState(BaseModel):
    id: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()