from langgraph.graph.state import StateGraph, END, START

from nodes.greeting_node import greeting_node
from nodes.pro_debator_node import pro_debator_node
from nodes.planning_node import planning_node
from nodes.search_web import search_web
from nodes.search_wikipedia import search_wikipedia
from nodes.anti_debator_node import anti_debator_node
from nodes.debate_summarize_node import debate_summarizer_node
from nodes.winner_decider_node import winner_decider_node

from router_functions.planner_and_pro_router import planner_and_pro_router
from router_functions.iteration_router import iteration_router
from router_functions.pro_and_anti_decider_router import pro_and_anti_decider_router

from states.agent_state import State

def debate_agent(memory, state):
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("Greetings", greeting_node)
    builder.add_node("Pro Debator", pro_debator_node)
    builder.add_node("Planner", planning_node)
    builder.add_node("Search Web", search_web)
    builder.add_node("Search Wikipedia", search_wikipedia)
    builder.add_node("Anti Debator", anti_debator_node)
    builder.add_node("Debate Summarizer", debate_summarizer_node)
    builder.add_node('Winner Decider', winner_decider_node)

    # Add edges
    builder.add_edge(START, "Greetings")
    builder.add_conditional_edges("Greetings", planner_and_pro_router, ['Planner', 'Pro Debator'])
    builder.add_edge("Planner", "Search Web")
    builder.add_edge("Planner", "Search Wikipedia")
    builder.add_conditional_edges("Search Web", pro_and_anti_decider_router, ["Pro Debator", "Anti Debator"])
    builder.add_conditional_edges("Search Wikipedia", pro_and_anti_decider_router, ["Pro Debator", "Anti Debator"])
    builder.add_edge("Pro Debator", "Planner")
    builder.add_edge("Anti Debator", "Debate Summarizer")
    builder.add_conditional_edges(
        "Debate Summarizer",
        iteration_router,
        ["Planner", "Winner Decider"]
    )
    builder.add_edge("Winner Decider", END)


    # Compile the graph
    debator = builder.compile(checkpointer=memory).with_config(run_name="Starting Debate")
    thread = {"configurable": {"thread_id": "1", "recursion_limit": 100}}
    result = debator.invoke(state, thread)
    return result['debate']

