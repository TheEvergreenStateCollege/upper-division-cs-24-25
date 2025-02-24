# Bellman Optimality Equation Function
def optimal_value(state, depth=0):
    # Set to negative infinity to be replaced on first comparison
    max_value = float('-inf')
    if depth < 1:
        return rewards[state] # Base case
    # Compare the value of each possible action
    probability = 1 / len(actions)
    for action in actions:
        if state + action not in states:
            continue
        state_value = 0
        for state_prime in states:
            reward = rewards[index]
            optimal = optimal_value(state_prime, depth-1)
            state_value += discount * probability * optimal
        # Keep track of the largest estimate
        max_value = max(max_value, state_value)
    return max_value

# Starting Inputs:
states = range(5) # List of states
rewards = [1, 0, 0, 0, -1] # Reward locations
actions = [-1, 1] # Move left, move right
discount = 0.9 # Falloff over distance
depth = 4 # Recursive depth of calculations

# Dictionary of each action at each state
policy = {}
# Build policy from actions and states
# (state, action): (next_state, reward)
for state in states:
    for action in actions:
        identifier = (state, action)
        next_state = state + action
        if next_state not in states:
            policy[identifier] = None
            continue
        probability = rewards[next_state]
        policy[identifier] = (next_state, reward)

for state in states:
    optimal = optimal_value(state, depth)
    print(optimal)
