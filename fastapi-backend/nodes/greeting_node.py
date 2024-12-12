import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from states.agent_state import State

load_dotenv()

def greeting_node(state: State):
    """LangGraph node that greets the debaters and introduces them"""

    google_api_key = os.getenv("GOOGLE_API_KEY")
    gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                            api_key=google_api_key
                            )

    topic = state['topic']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']

    prompt = f"""
        You are a professional and unbiased debate host introducing a formal debate.

        Participants:
        - Pro Debator: {pro_debator}, supporting the topic.
        - Anti Debator: {anti_debator}, opposing the topic.
        
        Topic: "{topic}"

        Instructions:
        * Begin by welcoming the audience.
        * Briefly introduce the participants and their positions like you are hosting a
        show. Briefly introduce the topic and what is at stake
        * Clearly state the topic of the debate.

        Keep the tone formal and neutral. Avoid opinions, commentary, or humor. 
        Keep the introduction concise.
    """
    greetings = gemini_model.invoke(prompt).content

    response = SystemMessage(
        content=greetings,
        name="greeting"
    )

    state['debate'].append(response)
    return state