# Bellman Optimality Equation Function
def optimal_value(state, depth=1):
    # Set to negative infinity to be replaced on first comparison
    max_value = float('-inf')
    for action in actions:
        state_value = 0
        for state_prime in states:
            for reward in rewards:
                ratio = probability(state_prime, reward, state, action)
                optimal = optimal_value(state_prime, depth-1)
                state_value += discount * probability * optimal
        # Keep track of the largest estimate
        max_value = max(max_value, state_estimate)
    return max_value

# Starting Inputs:
states = [-1, 2, 5, 10] # Policy evaluation of actions
rewards = [1, 0, 0, -1] # Reward from current state
discount = 0.9 # Falloff over distance
depth = 6 # Recursive depth of calculations

for state in states:
    optimal = optimal_value(state, depth)
    print(optimal)
