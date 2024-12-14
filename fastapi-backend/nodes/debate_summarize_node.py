import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from states.agent_state import State

def debate_summarizer_node(state: State):
  """LangGraph node that summarizes the exchange of arguments between debator
      and append to history for future consideration
  """

  model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
  )

  pro_debator = state['pro_debator']
  anti_debator = state['anti_debator']
  debate_history = state['debate_history']
  anti_debator_response = state['anti_debator_response']
  pro_debator_response = state['pro_debator_response']
  
  prompt = """
    You are an AI debate summarizer tasked with analyzing and summarizing the 
    latest exchange between two debaters: {pro_debator} and 
    {anti_debator} .  
    Your role is to create a concise and accurate summary of their arguments, 
    capturing the essence of the discussion for future reference.  

    **Instructions:**  
    1. **Focus on Key Points**: Highlight the central arguments presented by 
    each debater.  
    2. **Compare and Contrast**: Identify areas of agreement, if any, and key 
    disagreements or rebuttals.  
    3. **Clarity and Objectivity**: Ensure the summary is neutral, objective, 
    and easy to understand. Avoid injecting opinions or commentary.  
    4. **Avoid Irrelevance**: Discard repetitive, redundant, or irrelevant 
    details to keep the summary concise.  
    5. **Support Debate Continuity**: Ensure the summary can help in understanding 
    the flow of arguments for future use.  

    **Structure:**  
    1. **Pro Debator's Key Points:**  
      - Summarize {pro_debator}'s main arguments or rebuttals from the latest exchange.  
    2. **Anti Debator's Key Points:**  
      - Summarize {anti_debator}'s main arguments or rebuttals from the latest exchange.  
    
    **Inputs for Summary:**  
    - **Pro Debator's Latest Response:**  
      {pro_debator_response}  
    - **Anti Debator's Latest Response:**  
      {anti_debator_response}  

    Craft a well-structured and concise summary that captures the essence of this exchange.
  """
  system_message = prompt.format(
                      pro_debator=pro_debator,
                      pro_debator_response=pro_debator_response,
                      anti_debator=anti_debator,
                      anti_debator_response=anti_debator_response,
                    )
  summary = model.invoke(system_message).content
  debate_history.append(summary)
  state['debate_history'] = debate_history
  print(f"Updated Iteration: {state['iteration']}")
  return state

