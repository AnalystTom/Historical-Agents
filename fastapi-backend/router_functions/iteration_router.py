from states.agent_state import State

def iteration_router(state: State):
  """Routes the flow based on the current iteration and max_iteration"""
  if state['iteration'] >= state['max_iteration']:
      print("Ending the debate as max iteration is reached.")
      return "Debate Summarizer"
  print(f"Iteration Round: {state['iteration']}")
  state['iteration'] += 1
  return "Planner"