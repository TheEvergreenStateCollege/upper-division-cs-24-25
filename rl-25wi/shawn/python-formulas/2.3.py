# Temporal Difference Function
def get_estimate(reward=0, expectation=0, iteration=1):
    # Difference between current reward and expectation
    difference = reward - expectation
    # Proportion of this iteration to the total
    ratio = 1 / iteration
    # New estimate = old estimate + proportional difference
    return expectation + ratio * difference

# Starting Inputs:
sample_rewards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
estimate = 0

# Loop over rewards, adjusting the estimate each time
for iteration, reward in enumerate(sample_rewards, start=1):
    estimate = get_estimate(reward, estimate, iteration)
    print(estimate) # Print to show progress
