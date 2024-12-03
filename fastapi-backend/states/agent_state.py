from langgraph.graph.message import add_messages

from typing_extensions import TypedDict, Annotated

from .additional_states import DebateHistory, ProDebateResponse, AntiDebateResponse

class State(TypedDict):
    """
    Represents the state of the agent.
    """
    topic: str
    pro_debator: str
    anti_debator: str
    greetings: str
    pro_debator_response: ProDebateResponse
    anti_debator_response: AntiDebateResponse
    context: Annotated[list, add_messages]
    debate: Annotated[list, add_messages]
    debate_history: DebateHistory
    planner: str
    winner: str
    iteration: int
    max_iteration: int