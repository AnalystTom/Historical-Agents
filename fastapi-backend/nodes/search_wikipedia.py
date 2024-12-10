import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.messages import AIMessage, HumanMessage
from states.agent_state import State
def search_wikipedia(state: State):
    """Retrieve docs from Wikipedia using WikipediaRetriever with optimized token usage"""
    
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Simplified prompt templates
    pro_template = f"Generate a focused Wikipedia search query about {state['topic']} related to {state['pro_debator']}"
    anti_template = f"Generate a focused Wikipedia search query about {state['topic']} related to {state['anti_debator']}"
    
    # Choose template based on last message type
    search_query_prompt = pro_template if isinstance(state["debate"][-1], HumanMessage) else anti_template

    # Get search query
    search_query = model.invoke(search_query_prompt).content.strip()

    # Configure retriever with limits
    retriever = WikipediaRetriever(
        doc_content_chars_max=250,  # Limit character length
        load_max_docs=1,             # Limit number of documents
        load_all_available_meta=False # Only load essential metadata
    )

    # Get documents
    search_docs = retriever.invoke(search_query)

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