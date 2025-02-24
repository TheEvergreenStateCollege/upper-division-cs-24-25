# Temporal Difference Function
def get_estimates(rewards=[], estimate=0):
    iteration = 1
    # Loop over the rewards, adjusting the estimate each time
    for reward in rewards:
        # Proportion of this iteration to the total
        ratio = 1 / iteration
        # Difference between current reward and expectation
        difference = reward - estimate
        # New estimate = old estimate + proportional difference
        estimate += ratio * difference
        yield estimate
        iteration += 1

# Starting Inputs:
sample_rewards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
starting_value = 0 # Starting estimate

for estimate in get_estimates(sample_rewards, starting_value):
    print(estimate) # Print to show progress
