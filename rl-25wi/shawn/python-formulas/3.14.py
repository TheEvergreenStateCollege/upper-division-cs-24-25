# Bellman Equation Function
def get_estimate(reward=0, states=[0], discount=0.9):
    # Probability of taking each action (if chosen randomly)
    ratio = 1.0 / len(states)
    # Start estimate with current reward
    estimate = reward
    # Loop over all potential actions
    for action in states:
        # Add proportional value to the estimate
        estimate += ratio * action * discount
    return estimate

# Starting Inputs:
states = [-1, 2, 5, 10] # Policy evaluation of actions
reward = 1 # Reward from current state
discount = 0.9 # Falloff over distance

estimate = get_estimate(reward, states, discount)
print(estimate)
