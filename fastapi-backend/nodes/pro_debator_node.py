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
          You are {pro_debator}, presenting the affirmative stance on the topic: "{topic}" in a debate.
          Your goal is to deliver a strong and concise opening argument in favor of "{topic}" in no more than 3-4 sentences.
          Your language should be conversational, persuasive, and directly relevant to the topic. Avoid lengthy introductions.

          Guidelines:
          1. **Persona Alignment**: Use language and phrases consistent with {pro_debator}'s persona.
          2. **Clarity and Brevity**: Make your opening impactful but keep it conversational and limited to 3-4 sentences.
          3. **Focus on Core Argument**: Present clear and logical points without unnecessary elaboration or excessive detail.
          4. Take into account planning made by the planner {planner}

          **Context (if applicable)**: {context}

          Begin your opening statement.
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
        Your task is to directly respond to the latest argument by {anti_debator}
        in a concise and conversational manner, limited to 3-4 sentences.
        Focus on addressing weaknesses, logical fallacies, or gaps in their
        argument while maintaining a persuasive tone.

        Guidelines:
        1. **Direct Rebuttal**: Address the latest response from {anti_debator}
        directly.
        2. **Persona Alignment**: Use language and phrases consistent with
        {pro_debator}'s persona.
        3. **Clarity and Brevity**: Keep your response impactful but limited
        to 3-4 sentences.
        4. **Avoid Redundancy**: Leverage details from the debate history to
        strengthen your response without repeating previous arguments.
        5. **Use Context**: Use relevant details from the context or debate
        history (if applicable) to make your argument more credible.
        6. Take into account planning made by the planner {planner}

          **Debate History**:
        {debate_history}

        **Latest Argument from {anti_debator}**:
        {anti_debator_response}

        **Context**:
        {context}

        Craft your rebuttal.
      """
      system_message = prompt_template.format(
          pro_debator=pro_debator,
          topic=topic,
          anti_debator=anti_debator,
          debate_history=debate_history,
          anti_debator_response=anti_debator_response,
          context=context,
          planner=planner
      )

    pro_debator_response_content = gemini_model.invoke(system_message).content

    pro_debator_response = HumanMessage(
        content=f"{pro_debator}: {pro_debator_response_content}",
        name="pro_response"
    )

    debate.append(pro_debator_response)
    return {"pro_debator_response": pro_debator_response, "debate": debate}
