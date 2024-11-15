# Debate Crew

Welcome to the Debate Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Attention

This is template for designing...Please modify according to your use case.


- [Open Crew Flow Plot](./crewai_flow.html)

## Installating

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/flow_template/crews/{crew_name}/config/agents.yaml` to define your agents
- Modify `src/flow_template/crews/{crew_name}/config/tasks.yaml` to define your tasks
- Modify `src/flow_template/crews/main.py` to add custom inputs for your agents and tasks
- Modify `src/flow_template/crew.py` to add your own logic, tools and specific args


## Starting the Backend Server
From the root directory of your project, run the following command to start the backend server:

```bash
uvicorn src.flow_template.main:app --reload
```
This command initializes the FastAPI application, which handles WebSocket connections and facilitates the AI debate logic.

## Launching the Frontend Interface

Open the Frontend File

- Locate the index.html file in your project directory.
- Open the file in a web browser (e.g., Chrome, Firefox).
- Fill in the debate topic, debater names, and the maximum number of iterations.
- Click the "Start Debate" button to initiate the debate session.



Note: Ensure the backend server is running before starting the debate.


------------------------------------------------------------------------------------


## To DO

- Memory Management
- Fetching Input style details or relevant information from MongoDB
- Finalize number of crews, agents in each crew, tasks for each agents.


