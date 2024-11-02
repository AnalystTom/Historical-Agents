
from debate.crew import DebateCrew

def run():
    """
    Run the debate crew.
    """
    # Prompt the user for inputs
    topic = input("Please enter the debate topic: ")

    debater_a_name = input("Please enter the name of Debater A (famous person): ")

    debater_b_name = input("Please enter the name of Debater B (famous person): ")

    inputs = {
        'topic': topic,
        'debater_a_name': debater_a_name,
        'debater_b_name': debater_b_name
    }

    DebateCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
