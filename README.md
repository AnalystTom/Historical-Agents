
# Debate Crew

Welcome to the Debate Crew project, powered by [crewAI](https://crewai.com). This project is designed to simulate a debate between two famous individuals, allowing you to input the debate topic and select the debaters. The system leverages the powerful and flexible framework provided by crewAI to create a multi-agent AI system where agents collaborate effectively on complex tasks.

## Installation

Ensure you have **Python >=3.10 <=3.13** installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install `uv`:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

## Setting Up

**Add your `OPENAI_API_KEY` to the `.env` file**

Create a `.env` file in the root directory of your project and add the following line:

```
OPENAI_API_KEY=your-openai-api-key
```

Replace `your-openai-api-key` with your actual OpenAI API key.

## Running the Project

To kickstart your crew of AI agents and begin the debate simulation, run the following command from the root folder of your project:

```bash
crewai run
```

Alternatively, you can run the main script directly:

```bash
python src/debate/main.py
```

The program will prompt you to enter:

- **The debate topic**
- **The name of Debater A (a famous person)**
- **The name of Debater B (a famous person)**

**Example Interaction:**

```
Please enter the debate topic: The ethics of artificial intelligence
Please enter the name of Debater A (famous person): Alan Turing
Please enter the name of Debater B (famous person): Ada Lovelace
```

The system will then simulate a debate between the two selected individuals, adopting their personas and debating styles, and present the debate in multiple rounds. At the end of the debate, the moderator will declare a winner and provide justification.

## Understanding Your Crew

The Debate Crew is composed of multiple AI agents, each with unique roles and goals:

- **Moderator**: Facilitates the debate, verifies the qualifications of the debaters, and declares the winner.
- **Debater A**: Takes on the persona of the first famous person you select.
- **Debater B**: Takes on the persona of the second famous person you select.

These agents collaborate on a series of tasks defined in `src/debate/config/tasks.yaml`, leveraging their collective skills to simulate a realistic debate.

## Customizing

You can customize the agents and tasks to suit your needs:

- **Agents**: Modify `src/debate/config/agents.yaml` to define or adjust the agents' roles, goals, and backstories.
- **Tasks**: Modify `src/debate/config/tasks.yaml` to define or adjust the tasks the agents will perform.
- **Logic**: Modify `src/debate/crew.py` to add your own logic, tools, and specific arguments.
- **Inputs**: Modify `src/debate/main.py` if you want to change how the program accepts inputs.



---