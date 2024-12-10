import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchResults

from states.agent_state import State

load_dotenv()

def search_web(state: State):
    """LangGraph node that do a DuckDuckGo search and append the results to context."""

    model = ChatGroq(
      model="llama-3.3-70b-versatile",
      temperature=0.5,
      api_key=os.getenv("GROQ_API_KEY")
    )

    planner = state['planner']
    last_message = state['debate'][-1]

    prompt = f"""
        You are a search query generator for debate.
        Instructions:
        Based on the provided planning of the latest argument and the
        last message in a debate, generate a concise search query (maximum 8 words)
        focused on retrieving statistical and numerical data relevant to the latest prompt.
        Prioritize queries that are likely to yield objective data.
        Planning:
        {planner}

        Last Message:
        {last_message}
      """
    search_query = model.invoke(prompt).content.strip()

    print("DuckDuckGo Search Query:", search_query)

    search = DuckDuckGoSearchResults(backend="news", output_format='list')
    search_result = search.invoke(search_query)
    result = ""
    for entry in search_result:
        print(entry['snippet'])
        result += entry['snippet'] + "\n"

    state['context'].append(result)
    return {"context": state['context']}