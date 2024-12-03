import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from ..states.agent_state import State

load_dotenv()

def winner_decider_node(state: State):
  """LangGraph node that determines the winner of the debate"""

  model = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
  )
  
  debate_history = state['debate_history']
  prompt = """
    You are an AI judge tasked with determining the winner of a debate between
    two debaters based on their debate history.
    Analyze the provided debate history and determine which debater presented
    more logical and compelling arguments.
    Consider the following criteria:
    * **Logical consistency:** Does the debater's argumentation follow a clear
    and consistent line of reasoning? Are there any internal contradictions or
    logical fallacies?
    * **Evidence and support:** Does the debater provide sufficient evidence and
    support for their claims? Are the sources credible and relevant?
    * **Rebuttals and counterarguments:** How effectively does the debater
    address the opponent's arguments? Do they offer strong rebuttals and
    counterarguments?
    * **Clarity and persuasiveness:** Is the debater's communication clear,
    concise, and persuasive? Do they effectively convey their points to the
    audience?
    * **Overall impact:** Which debater's arguments had a greater overall impact
    and persuaded you more effectively?
    Debate History:
    {debate_history}
    Based on the debate history, who presented the more logical and stronger arguments: {pro_debator} or {anti_debator}?  Explain your reasoning by referencing specific instances from the debate history.  Provide a concise summary of why you chose the winner.  Do not simply restate the arguments.
  """
  system_message = prompt.format(
    debate_history=debate_history,
    pro_debator=state['pro_debator'],
    anti_debator=state['anti_debator']
  )
  winner = model.invoke(system_message).content
  return {"winner": winner}