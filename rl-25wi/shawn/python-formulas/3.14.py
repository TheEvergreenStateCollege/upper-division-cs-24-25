# Bellman Equation Function
def get_estimate(reward=0, actions=[0], discount=0.9):
    # Start estimate with current reward
    estimate = reward
    # Loop over all potential actions
    for action in actions:
        # Probability of taking the action (if chosen randomly)
        probability = 1.0 / len(states) # Dependent on policy
        # Add proportional value to the estimate
        estimate += action * discount * probability
    return estimate

# Starting Inputs:
reward = 1 # Reward from the current state
actions = [-1, 2, 5, 10] # Policy evaluation of potential actions
discount = 0.9 # Falloff over distance

estimate = get_estimate(reward, actions, discount)
print(estimate)
