from ..states.agent_state import State

def planner_and_pro_router(state: State):
    """LangGraph node that routes to planner or pro debator based on debate history"""
    debate_history = state["debate_history"]
    if debate_history == []:
        return "Pro Debator"
    else:
      return "Planner"