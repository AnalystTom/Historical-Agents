import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from ..states.agent_state import State

def debate_summarizer_node(state: State):
  """LangGraph node that summarizes the exchange of arguments between debator
      and append to history for future consideration
  """

  model = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    api_key=os.getenv("GROQ_API_KEY")
  )

  pro_debator = state['pro_debator']
  anti_debator = state['anti_debator']
  debate_history = state['debate_history']
  anti_debator_response = state['anti_debator_response']
  pro_debator_response = state['pro_debator_response']
  prompt = """
            Summarize the conversation between the pro {pro_debator} and anti debator {anti_debator},
            highlighting the key points of their arguments and discarding unnecessary points. The
            summary should be concise and brief, with high quality.
            **Instructions:**
            * Focus on the core arguments presented by both sides.
            * Identify the main points of agreement and disagreement.
            * Provide a clear and objective overview of the debate.
            * Avoid including irrelevant details or repetitive information.
            * Ensure that the summary is easy to understand and informative.
            **Pro Debator:**
            {pro_debator_response}
            **Anti Debator:**
            {anti_debator_response}
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
  state['iteration'] += 1
  print(f"Updated Iteration: {state['iteration']}")
  return state

