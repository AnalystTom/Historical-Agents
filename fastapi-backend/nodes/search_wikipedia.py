import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.messages import AIMessage, HumanMessage

from ..states.agent_state import State

def search_wikipedia(state: State):
    """Retrieve docs from Wikipedia using WikipediaRetriever"""

    model = ChatGroq(
      model="llama-3.1-70b-versatile",
      temperature=0.5,
      api_key=os.getenv("GROQ_API_KEY")
    )

    planner = state['planner']
    last_message = state["debate"][-1]
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    topic = state['topic']


    search_query_prompt = ""
    if isinstance(last_message, HumanMessage):
      search_query_prompt = f"""
        You are a search assistant generating a concise search query for Wikipedia.
        Task:
        Find the most relevant wikipedia articles for {pro_debator} related to
        the topic {topic} taking into account the following planning:
        {planner}
        Output:
        A single concise search query relevant to the topic.

        Given debater Trump and topic illegal immigration provide Immigration_policy_of_Donald_Trump
        as search query
      """
    elif isinstance(last_message, AIMessage):
      search_query_prompt = f"""
            You are a search assistant generating a concise search query for Wikipedia.
            Task:
            Find the most relevant wikipedia articles for {anti_debator} related to
            the topic {topic}
            Output:
            A single concise search query relevant to the topic.

           Given debater Trump and topic illegal immigration provide Immigration_policy_of_Donald_Trump
          as search query
          """

    search_query = model.invoke(search_query_prompt).content.strip()

    print(f'Search Query: {search_query}\n')

    retriever = WikipediaRetriever()

    search_docs = retriever.invoke(search_query)
    print(f'Search Docs: {search_docs}')

    all_summaries = ""
    for doc in search_docs:
        if 'summary' in doc.metadata:
            all_summaries += doc.metadata['summary'] + "\n\n"

    state['context'].append(all_summaries)
    print(f"Updated Context: {state['context']}")
    return state