import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from states.agent_state import State

load_dotenv()

def greeting_node(state: State):
    """LangGraph node that greets the debaters and introduces them"""

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    topic = state['topic']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']

    prompt = f"""
    You are a professional and unbiased debate host introducing a debate between two participants:

    {pro_debator}, who supports the topic.
    {anti_debator}, who opposes the topic.
    Topic: "{topic}"
    Instructions:
    Clearly and briefly introduce the participants and the topic to the audience.
    Avoid opinions, commentary, or humor. Maintain a formal and neutral tone.
    Do not include information not provided in this prompt. Keep the introduction concise, no more than 3 sentences.
    Ensure the output is free from errors or irrelevant content.
    Format:
    Start by welcoming the audience.
    Introduce the participants and their respective backgrounds.
    Introduce the topic of debate like a host.
    """
    greetings = model.invoke(prompt).content

    response = SystemMessage(
        content=greetings,
        name="greeting"
    )

    # pro_debator_response = HumanMessage(
    #     content=f"{pro_debator}: {pro_debator_response_content}",
    #     name="pro_response"
    # )

    state['debate'].append(response)
    return state