# GROUP:
# Shawn Bird
# Dawson White
# Austin Strayer
# Nicole Johnson
# Dani Monroe

import random
import matplotlib.pyplot as plt

# Number of arms/bandits
k = 10

# Epsilon/randomness rate
temp = 0.1

class Bandit:
    # Set mean for future pulls at init
    def __init__(self, mean):
        self.mean = mean
    def pull(self):
        # Get random reward within one standard deviation of the mean
        return random.gauss(self.mean, 1)

# Create a list of bandits with random means within one standard deviation of 0
bandits = [Bandit(random.gauss(0, 1)) for _ in range(k)]

# Print the bandit's true mean values
print("Real means:")
for i in range(k):
    print(i, bandits[i].mean)
print("---")

class Agent:
    # Track each estimate and count with lists indexed after the bandits
    def __init__(self):
        self.estimate = [0 for _ in range(k)]
        self.count = [0 for _ in range(k)]
        self.epsilon = temp
    # Integrate a new reward into the lists
    def process(self, i, r):
        p = self.estimate[i]
        c = self.count[i]
        if c < 1:
            c = 1 # Avoid divide by zero error
        # Temporal difference equation
        self.estimate[i] = p + (1 / c) * (r - p)
        self.count[i] = c + 1
    def step(self):
        index = 0
        # Pick a random bandit epsilon percent of the time
        if random.random() < self.epsilon:
            index = random.randint(0, k-1)
        # Otherwise use the bandit with the highest estimate
        else:
            index = self.estimate.index(max(self.estimate)) # Greedy
        # Generate a random reward and process it
        reward = bandits[index].pull()
        self.process(index, reward)
    # Run a series of steps
    def trial(self, count):
        self.accurracy = []
        optimal = max(bandits, key=lambda x: x.mean)
        for _ in range(count):
            a.step()
            ratio = max(a.estimate) / optimal.mean
            if ratio > 1:
                ratio = 2 - ratio
            self.accurracy.append(ratio)

# Single 1k step trial as demonstration
print("1000 step trial:")
a = Agent()
a.trial(1000)
for i in range(k):
    print(i, a.estimate[i], a.count[i])
plt.plot(range(len(a.accuracy)), a.accuracy)
plt.xlabel("Steps")
plt.ylabel("Accuracy")
plt.title("1000 Step Trial")
plt.show()
print("---")

# List to hold the results of each trial
averages = [[] for _ in range(k)]

# Run 2000 trials of 1000 steps each
for _ in range(2000):
    a = Agent()
    # Run 1000 steps and then add the estimates to the averages
    a.trial(1000)
    for i in range(k):
        averages[i].append(a.estimate[i])

print("Averages from 2000 trials:")
for i in range(k):
    print(i, sum(averages[i])/2000)
