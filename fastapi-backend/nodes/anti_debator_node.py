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
      model="llama-3.1-70b-versatile",
      temperature=0.5,
      api_key=os.getenv("GROQ_API_KEY")
    )

    topic = state['topic']
    anti_debator_response = state.get('anti_debator_response')
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    debate_history = state.get('debate_history', [])
    debate = state.get('debate', [])
    context = state.get('context', "")
    planner = state.get('planner', "")

    # Improved prompt with guardrails
    prompt_template = """
        You are {anti_debator}, presenting your opposing stance on the topic: "{topic}" in a debate.
        Your task is to craft a direct and concise rebuttal to the latest argument provided by {pro_debator}.
        The opinion should reflect a real stance that {anti_debator} has taken on the topic "{topic}" and align with their persona.

        Guidelines for crafting your rebuttal:
        1. **Direct Rebuttal**: Respond specifically to the latest argument from {pro_debator}. Address any logical flaws, missing evidence, or weak points while maintaining a respectful tone.
        2. **Clarity and Brevity**: Limit your response to no more than 3 sentences. Ensure it is conversational, impactful, and easy to follow.
        3. **Debate Continuity**: Use relevant details from the debate history (if provided) to strengthen your response while avoiding redundancy.
        4. **Persona Consistency**: Use language, phrases, and tone that align with {anti_debator}'s persona and style of communication.
        5. **Guardrails**: Avoid unsupported claims, personal attacks, or unrelated points. Stick to the topic and present logical arguments.
        6. **Use of Context**: Incorporate credible evidence or insights from the provided context (if applicable) to make your argument more persuasive.
        7. Take into account planning made by the planner {planner}

        **Context (if applicable)**:
        {context}

        **Debate History (recent exchanges)**:
        {debate_history}

        **Latest Argument from {pro_debator}**:
        {pro_debator_response}

        **Your Rebuttal**:
    """

    # Generate the system message for the model
    system_message = prompt_template.format(
        topic=topic,
        pro_debator=pro_debator,
        pro_debator_response=anti_debator_response,
        anti_debator=anti_debator,
        debate_history=debate_history,
        context=context,
        planner=planner
    )

    anti_debator_response_content = gemini_model.invoke(system_message).content

    anti_debator_response = AIMessage(
        content=f"{anti_debator}: {anti_debator_response_content}",
        name="anti_response"
    )

    debate.append(anti_debator_response)
    return {"anti_debator_response": anti_debator_response, "debate": debate}