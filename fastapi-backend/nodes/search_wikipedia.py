import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.messages import HumanMessage

from states.agent_state import State
from states.additional_states import SearchQuery

load_dotenv()

def search_wikipedia(state: State):
    """Retrieve docs from Wikipedia using WikipediaRetriever with optimized token usage"""
    
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    planner = state['planner']
    last_message = state["debate"][-1]
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    topic = state['topic']

    # Simplified prompt templates
    search_query_prompt = f"""
        You are a Wikipedia search assistant. Your task is to generate a concise, 
        relevant search query to retrieve the most accurate articles for the following 
        participant:
        - Debater: {pro_debator if isinstance(last_message, HumanMessage) else anti_debator}
        - Topic: {topic}
        - Planning Context: {planner}

        Deliverable: A single, 30 characters, concise query (e.g., "Immigration_policy_of_Donald_Trump")
        Note This is an example format only. Dont use it for answer.

        Ensure the query directly relates to the topic and reflects the debater's
        position.
    """
    structure_llm = model.with_structured_output(SearchQuery)
    search_query = structure_llm.invoke(search_query_prompt)

    # Configure retriever with limits
    retriever = WikipediaRetriever(
        doc_content_chars_max=250,  # Limit character length
        load_max_docs=1,             # Limit number of documents
        load_all_available_meta=False # Only load essential metadata
    )

    # Get documents
    search_docs = retriever.invoke(search_query.query)

    # Extract and combine summaries more efficiently
    summaries = []
    for doc in search_docs:
        if 'summary' in doc.metadata:
            # Take first 500 characters of each summary
            summaries.append(doc.metadata['summary'][:500])
    
    # Join summaries with single newline
    combined_summary = '\n'.join(summaries)
    
    # Update state with new context
    state['context'].append(combined_summary)
    
    return state