import os
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from states.agent_state import State

load_dotenv()

def planning_node(state: State):
    """LangGraph node that analyzes the latest argument and prepare a plan to come with a stronger argument"""

    model = ChatGroq(
      model="llama-3.3-70b-versatile",
      temperature=0.5,
      api_key=os.getenv("GROQ_API_KEY")
    )

    topic = state['topic']
    pro_debator = state['pro_debator']
    anti_debator = state['anti_debator']
    last_message = state["debate"][-1]
    planning_prompt = None

    system_message = ""

    if isinstance(last_message, HumanMessage):
      print("Planning for Anti Debator")
      planning_prompt = """
        You are an expert debate strategist tasked with helping {pro_debator} respond 
        to {anti_debator}'s argument on the topic: "{topic}".

        Input:
        * Anti-Debator's Argument: {last_message}

        Deliverable: A detailed plan with the following sections:
        1. **Identify Weaknesses**: Analyze the anti-debator's argument for logical 
        flaws or gaps.
        2. **Research Suggestions**: Recommend specific sources or keywords to support 
        your counterpoints.
        3. **Counter-Argument Strategy**: Provide a structured response that directly 
        addresses the weaknesses identified.
        4. **Rebuttal Preparation**: Anticipate potential rebuttals and suggest concise, 
        impactful counter-rebuttals.
        5. **Presentation Tips**: Offer suggestions for delivering the counter-argument 
        persuasively and effectively.
      """

      system_message = planning_prompt.format(
          topic=topic,
          anti_debator=anti_debator,
          pro_debator = pro_debator,
          last_message=last_message,
      )

    elif isinstance(last_message, AIMessage):
      # Analysis for an AIMessage (anti-debator's counterargument)
      print("Analyzing for Pro Debator")
      planning_prompt = """
        You are an expert debate strategist tasked with formulating a
        counter-argument
        against an opponent's position on a given topic.  Your goal is to
        create an actionable plan to devise a compelling and effective
        counter-argument for {anti_debator} against {pro_debator}.
        Given the following information:
        1. **Topic:** {topic}
        2. **Anti-Debator's Argument:** {last_message}
        4. **Desired Outcome:** Develop a counter-argument that effectively
        refutes the opponent's claims, strengthens your own position, and
        persuades the audience.


        **Develop an actionable plan that includes the following:**

        * **Identify Key Weaknesses:** Analyze the opponent's argument for
        logical fallacies, weak points, unsupported claims, or inconsistencies.
        List at least 3 key weaknesses.
        * **Research & Evidence Gathering:** Specify relevant areas of research,
        data sources, or examples that can be used to support your counter-argument.
        * **Counter-Argument Formulation:**  Outline the structure of your
        counter-argument.  Include the key points you will make and how they
        directly address the weaknesses identified.
        * **Rebuttals:** Anticipate potential rebuttals from the opponent and
        formulate concise responses.
        * **Presentation Strategy:**  Suggest how to effectively present your
        counter-argument, considering factors such as tone, clarity, and
        persuasive language.
        **Deliverable:** A detailed, step-by-step plan that can be used to
        create a powerful and persuasive counter-argument.
      """
      system_message = planning_prompt.format(
          topic=topic,
          anti_debator=anti_debator,
          pro_debator = pro_debator,
          last_message=last_message
      )
    state['planner'] = model.invoke(system_message).content
    return state