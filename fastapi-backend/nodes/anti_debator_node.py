import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from states.agent_state import State

load_dotenv()

def anti_debator_node(state: State):
    """LangGraph node that represents the anti debator"""

    gemini_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    topic = state["topic"]
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    pro_debator_response = state['pro_debator_response']
    debate_history = state.get('debate_history', [])
    planner = state.get('planner', "")
    context = state.get('context', [])
    debate = state.get('debate', [])

    # Improved prompt with guardrails
    prompt_template = """
        You are {anti_debator}, presenting your opposing stance on the topic: 
        "{topic}" in a debate.  
        Your task is to deliver concise, logical, and persuasive arguments to 
        challenge {pro_debator}'s position and refute their claims effectively.

        - Address the latest points raised by 
        {pro_debator} in **3-4 sentences**.  
        - Focus on dismantling their arguments by highlighting logical flaws, 
        inconsistencies, unsupported claims, or weaknesses, and provide counterpoints.  
        - Maintain a respectful yet assertive tone.  

        **General Guidelines:**  
        1. **Persona Alignment**: Use language and phrases consistent with 
        {anti_debator}'s persona and known debate style.  
        2. **Clarity and Brevity**: Ensure arguments are precise, logical, 
        and impactful.  
        3. **Debate Continuity**: Use relevant points from the debate history 
        to build stronger responses.  
        4. **Planning Context**: Incorporate strategies and insights from the 
        planning stage ({planner}), results of web and wikipedia search 
        {context}
        ..  

        **Debate History **  
        {debate_history}  

        **Latest Argument from {pro_debator}:**  
        {pro_debator_response}  
    """

    # Generate the system message for the model
    system_message = prompt_template.format(
        topic=topic,
        pro_debator=pro_debator,
        pro_debator_response=pro_debator_response,
        anti_debator=anti_debator,
        debate_history=debate_history,
        context=context,
        planner=planner
    )

    anti_debator_response_content = gemini_model.invoke(system_message).content

    anti_debator_response = AIMessage(
        content=f"{anti_debator_response_content}",
        name="anti_response"
    )

    state['anti_debator_response'] = anti_debator_response
    state["debate"].append(anti_debator_response)
    state['context']= []

    print(f"Context at Anti Debator: {state['context']}")

    return state