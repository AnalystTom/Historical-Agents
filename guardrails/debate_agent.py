from IPython.display import Image, display, Markdown
import textwrap
import os
import getpass
import time

from typing import Any, Annotated, List, TypedDict
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import get_buffer_string, AIMessage, HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.retrievers import WikipediaRetriever
from langchain_groq import ChatGroq

from langgraph.graph import MessagesState
from langgraph.graph.state import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

import getpass
import os

os.environ["TAVILY_API_KEY"] = getpass.getpass()


api_key = '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'
TAVILY_API_KEY='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'

model = ChatGroq(
    model="llama-3.2-1b-preview",
    verbose=True,
    temperature=0.5,
    api_key=api_key
)


memory = MemorySaver()

class State(TypedDict):
  topic: str
  pro_debator: str
  anti_debator: str
  greetings: str
  analysis: str
  pro_debator_response: str
  anti_debator_response: str
  context: Annotated[list, add_messages]
  debate: Annotated[list, add_messages]
  debate_history: List[str]
  iteration: int
  max_iteration: int

class SearchQuery(BaseModel):
    search_query: str = Field(description="The search query for retrieval")

structure_llm = model.with_structured_output(SearchQuery)
#structure_llm

def measure_time(node_function):
    """Decorator to measure and log the execution time of a node function."""
    def wrapper(state, *args, **kwargs):
        start_time = time.time()
        print(f"Starting node: {node_function.__name__}")
        result = node_function(state, *args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Node {node_function.__name__} completed in {elapsed_time:.2f} seconds.\n")

        # Optionally store in state for later analysis
        if "node_times" not in state:
            state["node_times"] = {}
        state["node_times"][node_function.__name__] = elapsed_time

        return result
    return wrapper


@measure_time
def greeting_node(state: State):
  """LangGraph node that greets the debators and introduces them"""
  print("Greeting Node")
  topic = state['topic']
  pro_debator = state['pro_debator']
  anti_debator = state['anti_debator']

  prompt = f"""You are hosting a debate between {pro_debator} and {anti_debator}
            on the topic {topic}. {pro_debator} is pro while {anti_debator} is
            against. You have to introduce the topic and debators to the audience.
            Your response should be short and conversational
            """

  greetings = model.invoke(prompt).content
  return {"greetings": greetings}


@measure_time
def analyzer_node(state: State):
    """LangGraph node that analyzes the latest argument for web search"""
    print("Analyzer Node")
    topic = state['topic']
    debate = state['debate']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    last_message = debate[-1]
    analysis_prompt = None
    if isinstance(last_message, HumanMessage):
        # Generate a prompt for a HumanMessage (pro-debator)
        print("Analyzing for Anti Debator")
        analysis_prompt = f"""
        Analyze the latest argument made by the pro-debator {pro_debator}  on the topic "{topic}".
        Focus on its strengths, weaknesses, and logical coherence. Write a short and concise
        analytical guidance that can be used for web search to help {anti_debator} better answer the argument
        and more completely support their stance on the topic {topic}. Keep the analysis as short as possible
        without losing quality.
        **Pro-Debator's Argument:**
        {last_message.content}
        """

    elif isinstance(last_message, AIMessage):
        # Generate a prompt for an AIMessage (anti-debator)
        print("Analyzing for Pro Debator")
        analysis_prompt = f"""
        Analyze the latest counterargument made by the anti-debator {anti_debator} on the topic "{topic}".
        Identify key points of contention and evaluate their validity.  Write a short and concise
        analytical guidance that can be used for web search to help {anti_debator} to effectively refute these arguments
        and more completely support their stance on the topic {topic}. Keep the analysis as short as possible
        without losing quality.
        **Anti-Debator's Counterargument:**
        {last_message.content}
        """

    analysis = model.invoke(analysis_prompt).content
    return {"analysis": analysis}

@measure_time
def search_web(state: State):
    """LangGraph node to search the web using Tavily Search API and append the results to context."""
    analysis = state['analysis']

    context = state['context']

    # Generate Search Query
    search_query = model.invoke(
        f"Generate a web search query using analysis {analysis} and debate history {state['debate_history']}. the search query should be no longer than 3 sentences"
    ).content
    print("Tavily Search Query:", search_query)
    tavily_search = TavilySearchResults(
                      max_results=2,
                      include_answer=True,
                      include_raw_content=True

                      # search_depth="advanced",
                      # include_domains = []
                      # exclude_domains = []
                  )
    search_docs = tavily_search.invoke(search_query)
    print("search_docs:", search_docs)

    # Check if `search_docs` contains valid dictionaries
    if isinstance(search_docs, list) and all(isinstance(doc, dict) for doc in search_docs):
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f"**URL:** {doc.get('url', 'No URL')}\n**Content:** {doc.get('content', 'No Content')}"
                for doc in search_docs
            ]
        )
    elif isinstance(search_docs, list) and all(isinstance(doc, str) for doc in search_docs):
        formatted_search_docs = "\n\n---\n\n".join(search_docs)
    else:
        formatted_search_docs = "Search results are in an unexpected format."

    # Append to context
    context.append(formatted_search_docs)
    return {"context": context}

@measure_time
def search_wikipedia(state: State):
    """Retrieve docs from Wikipedia using WikipediaRetriever"""
    print("Searching Wikipedia")

    # Analysis and debate context
    analysis = state['analysis']
    debate_history = state['debate_history']
    print('analysis, debate_history',analysis, debate_history)
    search_query = model.invoke(
        f"Generate a wikipedia search query using analysis {analysis} and debate history {state['debate_history']}. the search query should be no longer than 1 sentences and search should be restricted to only 1 page. Please do share the page"
    ).content
    print("Wikipedia Search Query:", search_query)

    # WikipediaRetriever setup
    retriever = WikipediaRetriever()
    search_docs = retriever.get_relevant_documents(search_query)

    # Format the results
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f"\n{doc.page_content}\n"
            for doc in search_docs
        ]
    )

    print(f"Wikipedia DOcs: {formatted_search_docs}")
    return {"context": [formatted_search_docs]}

@measure_time
def router(state: State):
    """LangGraph node that routes to the appropriate search function"""
    debate_history = state["debate_history"]
    if debate_history == []:
        return "Pro Debator"
    else:
      return "Analyzer"

def iteration_router(state: State):
    """Routes the flow based on the current iteration and max_iteration"""

    if state['iteration'] <= state['max_iteration']:
        print(f"Iteration Round: {state['iteration']}")
        state['iteration'] = state['iteration'] + 1
        return "Analyzer"
    else:
        # End the debate
        return END

@measure_time
def analyzer_router(state: State):
    """Function that routes to the appropriate next node"""
    debate = state['debate']
    last_message = debate[-1]
    if isinstance(last_message, AIMessage):
        return "Pro Debator"  # Pro Debator responds to the anti-debator's argument
    else:
        return "Anti Debator"  # Anti Debator responds to the pro-debator's argument


@measure_time
def pro_debator_node(state: State):
    """LangGraph node that represents the pro debator"""

    print("Pro Debator Node")

    topic = state['topic']
    anti_debator_response = state['anti_debator_response']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    debate_history = state['debate_history']
    debate = state['debate']

    if anti_debator_response is None and debate == []:
        prompt_template = """
            You are {pro_debator}, a pro debator on the topic of {topic} having a debate with {anti_debator}.
            Your goal is to present compelling arguments in favor of {topic} while maintaining the persona of {pro_debator}.
            Ensure your responses are coherent, logical, and persuasive.
            Keep the persona of {pro_debator} throughout the entire conversation.
            Your responses should be relevant to the current stage of the debate.
            You can refute the other debator's arguments and present your own supporting evidence for {topic}.
            Do not deviate from your persona. Respond concisely and your response must be less than 4 sentences.
        """
        system_message = prompt_template.format(topic=topic, pro_debator=pro_debator, anti_debator=anti_debator)
        pro_debator_response_content = model.invoke(system_message).content
    else:
      context = state['context']
      prompt_template = """
          You are a professional debater, embodying the persona of {pro_debator}. Your goal is to convincingly argue the affirmative side of the debate topic: "{topic}".
          You must maintain your assigned persona throughout the debate and ensure that your arguments align with it.
          Remember the following:
          1. Respond to the latest argument of the anti-debator provided below, ensuring your response directly addresses their points.
          2. Consider the context of the debate history {debate_history} and data gathered from web search {context}, building upon your
          previous arguments and refuting the anti-debator's counterarguments effectively.
          3. Use eloquent and persuasive language, demonstrating your mastery of the topic and your persona.
          4. Avoid making factual errors or inconsistencies that might damage your credibility.
          5. Response should be less than 5 sentences
          **Debate History:**
          {debate_history}
          **Latest Anti-Debator Argument:**
          {anti_debator_response}
          **Your Response (Pro Debator):**
      """
      system_message = prompt_template.format(
          topic=topic,
          pro_debator=pro_debator,
          anti_debator=anti_debator,
          debate_history=debate_history,
          anti_debator_response=anti_debator_response,
          context=context
      )
      pro_debator_response_content = model.invoke(system_message).content

    # Create a HumanMessage with the response content and assign a name
    pro_debator_response = HumanMessage(
        content=f"""{pro_debator}: {pro_debator_response_content}""",
        name="pro_response"
    )

    debate.append(pro_debator_response)
    return {"pro_debator_response": pro_debator_response, "debate": debate}


@measure_time
def anti_debator_node(state: State):
    """LangGraph node that represents the anti debator"""
    print("Anti Debator Node")
    topic = state['topic']
    anti_debator_response = state['anti_debator_response']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    debate_history = state['debate_history']
    debate = state['debate']
    context = state['context']

    prompt_template = prompt_template = """
            You are {anti_debator}, an anti debator on the topic of {topic} having a debate with {pro_debator}.
            Your goal is to present compelling arguments against {pro_debator_response} on topic {topic} while maintaining the persona of {anti_debator}.
            Ensure your responses are coherent, logical, and persuasive.
            Keep the persona of {anti_debator} throughout the entire conversation.
            Your responses should be relevant to the current stage of the debate.
            You can refute the other debator's arguments and present your own supporting evidence against {topic}
            using the context {context} and history of debate {debate_history}.
            Do not deviate from your persona. Respond concisely in no more than 5 sentences.
        """
    system_message = prompt_template.format(
        topic=topic,
        pro_debator=pro_debator,
        pro_debator_response=anti_debator_response,
        anti_debator=anti_debator,
        debate_history=debate_history,
        anti_debator_response=anti_debator_response,
        context=context
    )
    pro_debator_response_content = model.invoke(system_message).content

    # Create a HumanMessage with the response content and assign a name
    anti_debator_response = AIMessage(
        content=f"""{anti_debator}: {pro_debator_response_content}""",
        name="pro_response"
    )

    debate.append(anti_debator_response)
    return {"anti_debator_response": anti_debator_response, "debate": debate}

@measure_time
def debate_summarizer_node(state: State):
  """LangGraph node that summarizes the exchange of arguments between debator
  and append to history for future consideration
  """
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
            * The summary should be approximately 1.
            **Pro Debator:**
            {pro_debator_response}
            **Anti Debator:**
            {anti_debator_response}
          """
  system_message = prompt.format(
                      pro_debator=pro_debator,
                      pro_debator_response=anti_debator_response,
                      anti_debator=anti_debator,
                      anti_debator_response=anti_debator_response,
                    )
  summary = model.invoke(system_message).content
  debate_history.append(summary)
  return {"debate_history": debate_history}


builder = StateGraph(State)

# Add nodes
builder.add_node("Greetings", greeting_node)
builder.add_node("Pro Debator", pro_debator_node)
builder.add_node("Analyzer", analyzer_node)
builder.add_node("Search Web", search_web)
builder.add_node("Search Wikipedia", search_wikipedia)
builder.add_node("Anti Debator", anti_debator_node)
builder.add_node("Debate Summarizer", debate_summarizer_node)

# Add edges
builder.add_edge(START, "Greetings")
builder.add_conditional_edges("Greetings", router, ['Analyzer', 'Pro Debator'])
builder.add_edge("Analyzer", "Search Web")
builder.add_edge("Analyzer", "Search Wikipedia")
builder.add_conditional_edges("Search Web", analyzer_router, ["Pro Debator", "Anti Debator"])
builder.add_conditional_edges("Search Wikipedia", analyzer_router, ["Pro Debator", "Anti Debator"])
builder.add_edge("Pro Debator", "Analyzer")
builder.add_edge("Anti Debator", "Debate Summarizer")
builder.add_edge("Debate Summarizer", END)

# Compile the graph
debator = builder.compile(checkpointer=memory).with_config(run_name="Create podcast")

# Display the graph
#display(Image(debator.get_graph().draw_mermaid_png()))


state = {
    "topic": "Illegal Immigrants",
    "pro_debator": "Joe Biden",
    "anti_debator": "Donald Trump",
    "greetings": "",
    "analysis": "",
    "pro_debator_response": "",
    "anti_debator_response": "",
    "context": [],
    "debate": [],
    "debate_history": [],
    "iteration": 0,
    "max_iteration": 1
}


thread = {"configurable": {"thread_id": "1"}}
result = debator.invoke(state, thread)
print(result)

import pprint
pprint.pprint(result['pro_debator_response'].content)

# pprint.pprint(result['anti_debator_response'].content)
# pprint.pprint(result['greetings'])
# pprint.pprint(result['analysis'])
# print(result['debate'])
