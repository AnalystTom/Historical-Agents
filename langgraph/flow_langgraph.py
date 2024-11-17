from typing import Dict, TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from functools import partial
from pymongo import MongoClient
from dotenv import load_dotenv
import os


#Replace <db_username> and <db_password> with your actual username and password
client = MongoClient("mongodb+srv://user:BUiIZW9wSnqgPbhN@histcluster.lijlj.mongodb.net/personaDB?retryWrites=true&w=majority")

#Specify database and collection
db = client["personaDB"]
Personas = db['Personas']

load_dotenv()

# Set up the LLM
llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), streaming=True)

# Define the GraphState for LangGraph
class GraphState(TypedDict):
    classification: Optional[str] = None
    history: Optional[str] = None
    current_response: Optional[str] = None
    count: Optional[int] = None
    results: Optional[str] = None
    greeting: Optional[str] = None
    debate_topic: Optional[str] = None
    debater1: Optional[str] = None
    debater2: Optional[str] = None

workflow = StateGraph(GraphState)


def get_character_persona(name):
    # Query the nested 'name' field within the 'historicalFigures' array
    character = Personas.find_one(
        {"historicalFigures.name": name},
        {"historicalFigures.$": 1}  # Project only the matching element in the array
    )
    
    if not character:
        raise ValueError(f"Character {name} not found in the database.")
    
    # Extract the first (and only) element from the 'historicalFigures' array
    persona = character['historicalFigures'][0]
    
    # Return the necessary details
    return {
        'name': persona['name'],
        'occupation': persona['occupation'],
        'tone': persona['tone'],
        'style': persona['style'],
        'quotes': persona.get('quotes', [])
    }
# Custom prompt for impersonation
# MAKE SURE THAT THE debater1 name passed through mathes the "name" variable in the mongoDB schema
def build_prefix(debater1, debater2, debate_topic, history, current_debater):
    persona1 = get_character_persona(debater1)
    persona2 = get_character_persona(debater2)

    # Determine which persona to use based on the current debater
    if current_debater == debater1:
        current_persona = persona1
        opponent_persona = persona2
    else:
        current_persona = persona2
        opponent_persona = persona1

    # Use the first quote for simplicity, or choose randomly
    try:
        quote1 = current_persona['quotes'][0]['Quote Content']
    except (IndexError, KeyError):
        quote1 = "No quote available"

    try:
        quote2 = opponent_persona['quotes'][0]['Quote Content']
    except (IndexError, KeyError):
        quote2 = "No quote available"

    prefix = f'''You are impersonating {current_persona['name']}  in a debate with {opponent_persona['name']} (Opp) on the topic: "{debate_topic}".
    {current_persona['name']} is a {current_persona['occupation']} known for his tone being {current_persona['tone']} and his style being {current_persona['style']}, an example of their quote is: "{quote1}".
    
    {opponent_persona['name']} is a {opponent_persona['occupation']} known for his tone being {opponent_persona['tone']} and his style being {opponent_persona['style']}, an example of their quote is: "{quote2}".
    The debate so far is as follows:

    {history}

    Be sure to start the debate with an ad hominem attack on the opponent.
    If history is present, respond to {opponent_persona['name']}'s arguments, taking into account their arguemnts and beliefs. 
    Be sure to escalate your arguments as the debate progresses. 
    Respond  in a manner consistent with {current_persona['name']}'s style and argumentation and account for the . 
    Provide a concise, impactful response that avoids repeating previous points.'''
    
    return prefix

# Function to classify sentiment of the input
def classify(question, debater1, debater2):
    return llm(f"classify the sentiment of input as {debater1.replace(' ', '_')} or {debater2.replace(' ', '_')}. Output just the class. Input: {question}").strip()

def classify_input_node(state):
    question = state.get('current_response')
    classification = classify(question, state['debater1'], state['debater2'])
    return {"classification": classification}

def handle_greeting_node(state):
    return {"greeting": f"Welcome! Today’s debate is between {state['debater1']} (Pro) and {state['debater2']} (Opp) on the topic of \"{state['debate_topic']}\"."}

def handle_pro(state):
    summary = state.get('history', '').strip()
    current_response = state.get('current_response', '').strip()
    prompt = build_prefix(state['debater1'], state['debater2'], state['debate_topic'], summary, state['debater1'])
    argument = f"{state['debater1']}: " + llm(prompt)
    return {"history": summary + '\n' + argument, "current_response": argument, "count": state.get('count', 0) + 1}

def handle_opp(state):
    summary = state.get('history', '').strip()
    current_response = state.get('current_response', '').strip()
    prompt = build_prefix(state['debater1'], state['debater2'], state['debate_topic'], summary, state['debater2'])
    argument = f"{state['debater2']}: " + llm(prompt)
    return {"history": summary + '\n' + argument, "current_response": argument, "count": state.get('count', 0) + 1}
def result(state):
    summary = state.get('history').strip()
    prompt = f"Summarize the conversation and judge who won the debate. No ties are allowed. Conversation: {summary}"
    return {"results": llm(prompt)}

# Define workflow nodes and edges
workflow.add_node("classify_input", classify_input_node)
workflow.add_node("handle_greeting", handle_greeting_node)
workflow.add_node("handle_pro", handle_pro)
workflow.add_node("handle_opp", handle_opp)
workflow.add_node("result", result)

def decide_next_node(state):
    # Alternate turns based on the count
    if state.get('count', 0) % 2 == 0:
        return "handle_pro"
    else:
        return "handle_opp"

def check_conv_length(state):
    return "result" if state.get("count", 0) == 4 else "classify_input"

workflow.add_conditional_edges(
    "classify_input",
    decide_next_node,
    {
        "handle_pro": "handle_pro",
        "handle_opp": "handle_opp"
    }
)

workflow.add_conditional_edges(
    "handle_pro",
    check_conv_length,
    {
        "result": "result",
        "classify_input": "classify_input"
    }
)

workflow.add_conditional_edges(
    "handle_opp",
    check_conv_length,
    {
        "result": "result",
        "classify_input": "classify_input"
    }
)

workflow.set_entry_point("handle_greeting")
workflow.add_edge('handle_greeting', "handle_pro")
workflow.add_edge('result', END)

# Compile the workflow
compiled_workflow = workflow.compile()

# Import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for the request body
class DebateRequest(BaseModel):
    count: int = 0
    history: str = "Nothing"
    current_response: str = ""
    debate_topic: str = ""
    debater1: str = ""
    debater2: str = ""

# Define an API endpoint
@app.post('/trigger_workflow')
async def trigger_workflow(request: DebateRequest):
    # Execute the workflow with the provided state
    conversation = compiled_workflow.invoke({
        'count': request.count,
        'history': request.history,
        'current_response': request.current_response,
        'debate_topic': request.debate_topic,
        'debater1': request.debater1,
        'debater2': request.debater2
    })

    # Return the history as a JSON response
    return {'history': conversation['history']}

# Run the FastAPI app using Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)