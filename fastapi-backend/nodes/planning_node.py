import os
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from ..states.agent_state import State

load_dotenv()

def planning_node(state: State):
    """LangGraph node that analyzes the latest argument for web search"""

    model = ChatGroq(
      model="llama-3.1-70b-versatile",
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
        You are an expert in debate strategy. Your task is to help the anti-debator
        {anti_debator} craft
        a compelling counter-argument to the pro-debator's, {pro_debator}, arguments on the debate topic:
        {topic}.
        Here's the information you have:
        * **Pro-Debator's Argument:** {last_message}
        Generate an actionable plan with the following structure:
        **1. Identify Weaknesses:** Analyze the pro-debator's argument. Pinpoint logical
        fallacies, weak points, unsupported claims, or areas where more evidence is needed.
        **2. Research and Evidence Gathering:** Suggest specific research avenues to find
        evidence that refutes the pro-debator's argument.  Provide concrete examples of
        sources and keywords.
        **3. Counter-Argument Formulation:** Outline the main points of a counter-argument.
        Each point should directly address a weakness in the pro-debator's argument and be
        supported by the suggested research.
        **4. Rebuttals:** Anticipate the pro-debator's possible rebuttals and suggest
        preemptive counter-rebuttals.
        **5. Presentation Strategy:** Outline how to present the counter-argument
        effectively:
            * Should the anti-debator focus on emotion or logic?
            * What rhetorical devices would be effective?
            * How to present the evidence concisely and persuasively?
        Example Output:
        **1. Identify Weaknesses:** The pro-debator's argument relies on a study from
        2010, which may be outdated.  They also don't address the economic impact of
        their proposal.

        **2. Research and Evidence Gathering:** Search for more recent studies on the
        topic. Look for economic analyses of similar proposals. Search terms: "[topic]
        economic impact," "[topic] recent studies," etc.  Look for credible sources
        such as peer-reviewed journals.
        **3. Counter-Argument Formulation:**
            * Point 1: The 2010 study is outdated and newer research contradicts its findings.
            * Point 2: The proposal has significant negative economic consequences.
        **4. Rebuttals:** The pro-debator might argue that the newer studies are biased.
        Prepare to address this by presenting evidence of the studies' methodology and
        peer review.
        **5. Presentation Strategy:** Emphasize the economic impact and present the data
        visually. Maintain a logical, calm demeanor. Use statistics and specific examples
        instead of generalizations.

        Ensure the plan is specific to the given information.
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