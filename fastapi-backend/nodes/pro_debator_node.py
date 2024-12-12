import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from states.agent_state import State

load_dotenv()

def pro_debator_node(state: State):
    """LangGraph node that represents the pro debator"""

    gemini_model = ChatGroq(
      model="llama-3.3-70b-versatile",
      temperature=0.5,
      api_key=os.getenv("GROQ_API_KEY")
    )

    topic = state['topic']
    anti_debator_response = state.get('anti_debator_response')
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    debate_history = state.get('debate_history', [])
    planner = state.get("planner", "")
    debate = state.get('debate', [])
    context = state.get('context', "")

    if not anti_debator_response and not debate:
      # Greeting and opening argument scenario
      prompt_template = """
        You are {pro_debator}, advocating for the affirmative position on the topic: 
        "{topic}".
        
        Deliverable: A strong and concise opening argument in favor of the topic 
        (3-4 sentences max). Maintain the public persona, rhetorical style, and 
        ideological clarity of {pro_debator}
        
        Guidelines:
        * Stay aligned with {pro_debator}'s persona and style.
        * Make the argument conversational, persuasive, and focused.
        * Stick to the topic {topic} and your persona, rhetorical style and ideology
        * Dont include any irrelevant things in the response like templates etc
      """
      system_message = prompt_template.format(
          pro_debator=pro_debator,
          anti_debator=anti_debator,
          planner=planner,
          topic=topic,
          context=context
      )
    else:
      # Responding to latest argument scenario
      prompt_template = """
        You are {pro_debator}, presenting your affirmative stance on the topic: 
        "{topic}" in a debate. 
        Your goal is to deliver strong, logical, and concise arguments that support 
        "{topic}" while persuading the audience of your position.

        - Address the latest points raised by {anti_debator} in **3-4 sentences**.  
        - Focus on refuting their arguments by highlighting logical flaws, 
        unsupported claims, or weaknesses, while presenting evidence to 
        strengthen your position.  
        - Maintain a conversational and persuasive tone.  

        **General Guidelines:**  
        1. **Persona Alignment**: Use language and phrases consistent with 
        {pro_debator}'s persona and known debate style.  
        2. **Clarity and Brevity**: Ensure arguments are logical, concise, and 
        impactful.  
        3. **Debate Continuity**: Use relevant points from the debate history 
        to avoid redundancy and add depth.  
        4. **Planning Context**: Take into account insights or strategies from 
        the planning stage ({planner}) and wikipedia and web search results {context}.  

        **Debate History :**  
        {debate_history}  

        **Latest Argument from {anti_debator}:**  
        {anti_debator_response}  

      """
      system_message = prompt_template.format(
        pro_debator=pro_debator,
        topic=topic,
        anti_debator=anti_debator,
        debate_history=debate_history,
        anti_debator_response=anti_debator_response,
        planner=planner,
        context=context
      )

    pro_debator_response_content = gemini_model.invoke(system_message).content

    pro_debator_response = HumanMessage(
        content=f"{pro_debator}: {pro_debator_response_content}",
        name="pro_response"
    )

    debate.append(pro_debator_response)
    return {"pro_debator_response": pro_debator_response, "debate": debate}
