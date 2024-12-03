from typing import List

from pydantic import BaseModel, Field

class DebateHistory(BaseModel):
  """A class that stores the history of a arguments of both side during debate."""
  debate_history: List[str] = Field(description="A variable that stores summary of every debate round")


class AntiDebateResponse(BaseModel):
  """A class that stores the most recent response of anti debator"""
  anti_debator_response: str = Field(description="The anti-debator's response to the latest argument")


class ProDebateResponse(BaseModel):
  """A class that stores the most recent response of pro debator"""
  pro_debator_response: str = Field(description="The pro-debator's response to the latest argument")