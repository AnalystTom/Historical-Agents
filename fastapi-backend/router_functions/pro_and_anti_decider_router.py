from langchain_core.messages import AIMessage

from states.agent_state import State

def pro_and_anti_decider_router(state: State):
    """Function that routes to the appropriate next node"""
    debate = state['debate']
    last_message = debate[-1]
    if isinstance(last_message, AIMessage):
        return "Pro Debator"
    else:
        return "Anti Debator"