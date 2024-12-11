from typing import List

from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    query: str = Field(description="The query to search for")
    
class DebateHistory(BaseModel):
  """A class that stores the history of a arguments of both side during debate."""
  debate_history: List[str] = Field(description="A variable that stores summary of every debate round")


class AntiDebateResponse(BaseModel):
  """A class that stores the most recent response of anti debator"""
  anti_debator_response: str = Field(description="The anti-debator's response to the latest argument")


class ProDebateResponse(BaseModel):
  """A class that stores the most recent response of pro debator"""
  pro_debator_response: str = Field(description="The pro-debator's response to the latest argument")

class WinnerResponse(BaseModel):
  winner: str = Field(description="The winner of the debate")
  clarity: str = Field(description="Explain how clear the responses of both debators were")
  clarity_score: List[int] = Field(description="Clarity score of pro and anti debator out of 10")
  persuasiveness: str = Field(description="Explain how persuasive both debators were")
  persuasion_score: List[int] = Field(description="Persuasiveness score of pro and anti debator out of 10")
  relevance: str = Field(description="Explain how relevant the arguments of both debators were")
  relevance_score: List[int] = Field(description="Relevance score of pro and anti debator out of 10")
  logical_soundness: str = Field(description="Explain how logical sound the arguments of both debators were")
  logical_soundness_score: List[int] = Field(description="Logical soundness score of pro and anti debator out of 10")