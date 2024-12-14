from typing import Optional, List, Dict, Any
from langgraph.graph.state import StateGraph, END, START, CompiledStateGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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

async def debate_agent(memory, state, websocket_manager):
    builder = StateGraph(State)

    # Add nodes
    builder.add_node("Pro Debator", lambda state: pro_debator_node(state, websocket_manager))
    builder.add_node("Anti Debator", lambda state: anti_debator_node(state, websocket_manager))
    builder.add_node("Greetings", greeting_node)
    builder.add_node("Planner", planning_node)
    builder.add_node("Search Web", search_web)
    builder.add_node("Search Wikipedia", search_wikipedia)
    builder.add_node("Debate Summarizer", debate_summarizer_node)
    builder.add_node("Winner Decider", winner_decider_node)

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

    debator = builder.compile(checkpointer=memory).with_config(run_name="Starting Debate")
    thread = {"configurable": {"thread_id": "1", "recursion_limit": 100}}
    
    conversation: List[Dict[str, str]] = []  # Initialize the conversation list
    previous_debate: List[Any] = []  # Track the previous debate state to avoid duplicates
    final_summary = None  # To hold the debate summary
    final_winner = None  # To hold the winner result

    try:
        for step in debator.stream(state, thread):
            if isinstance(step, dict) and step:
                node_name, node_data = next(iter(step.items()))
            else:
                print("Invalid step structure:", step)
                continue

            # Safely retrieve the debate variable
            debate = node_data.get('debate', [])
            if not isinstance(debate, list):
                print(f"Unexpected debate type at node '{node_name}': {type(debate)}")
                debate = []

            # Add only new messages to the conversation
            new_messages = [msg for msg in debate if msg not in previous_debate]
            previous_debate = debate  # Update the previous_debate to the latest state

            for item in new_messages:
                if isinstance(item, SystemMessage):
                    conversation.append({"type": "SystemMessage", "content": item.content})
                elif isinstance(item, HumanMessage):
                    conversation.append({"type": "HumanMessage", "content": item.content})
                elif isinstance(item, AIMessage):
                    conversation.append({"type": "AIMessage", "content": item.content})

            # Send updates only if there are new messages
            if new_messages:
                try:
                    # Extract the last message from the conversation
                    last_message = conversation[-1]
                    await websocket_manager.send_update(last_message["type"], last_message["content"])
                except Exception as e:
                    print(f"Error sending WebSocket update: {e}")

            # Capture final summary and winner data
            if node_name == "Debate Summarizer":
                final_summary = node_data.get('summary', None)
            if node_name == "Winner Decider":
                final_winner = node_data.get('winner', None)
    except Exception as e:
        print(f"Error during debate agent execution: {e}")
    finally:
        # Return the final summary and winner to the caller
        return {"summary": final_summary, "winner": final_winner}
