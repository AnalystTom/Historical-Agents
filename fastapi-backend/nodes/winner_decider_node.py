import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from states.agent_state import State
from states.additional_states import WinnerResponse

load_dotenv()

def winner_decider_node(state: State):
  """LangGraph node that determines the winner of the debate"""

  model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
  )
  
  debate_history = state['debate_history']
  prompt = """
    You are an AI judge determining the winner of a debate between {pro_debator} 
    and {anti_debator}. Also do a comparative analysis between both debators

    Criteria:
    * Logical consistency
    * Evidence and support
    * Effectiveness of rebuttals
    * Clarity and persuasiveness
    * Overall impact

    Input: Debate History: {debate_history}

    Deliverable: Identify the winner and provide a rationale with specific
    references to the debate history. Example format:
  """
  
  system_message = prompt.format(
    debate_history=debate_history,
    pro_debator=state['pro_debator'],
    anti_debator=state['anti_debator']
  )
  winner_content = model.invoke(system_message).content
    
  # Format the winner content to ensure numbered points are on new lines
  structure_llm = model.with_structured_output(WinnerResponse)
  winner = structure_llm.invoke(system_message)
  return {"winner": winner}


