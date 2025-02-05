import random
import numpy as np

SIZE     = 5   # Size of movable area
DEPTH    = 3   # Number of recursive estimates
DISCOUNT = 0.9 # Discount per square

# Assignment
# Goals: understand Markov decision processes by  simulation, in particular figure 3.2 gridworld
# Task: program the simulation in Python, where the agent and the environment are distinct.
# The agent uses a random policy where there are 4 actions in each state, and they are all equally likely
# A state is a pair of numbers, each between 0 and 4
# An action is a number 0 - 3
# The agent knows its state, and chooses an action. It keeps track of the average reward for
# The environment returns a reward and a new state
# Simulate 1000 steps. How well do the averages fit the values in Fig 3.2?

class Agent:
    def __init__(self, environment):
        self.states = {}
        self.states[(1, 1)] = self.State(1, 1)
        self.state = self.states[(1, 1)]
        self.actions = np.array([[0, -1], [1, 0], [0, 1], [-1, 0]])
        self.environment = environment

    class State:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.estimatedValue = 0.0
            # States are keyed into the dictionary with a tuple (x, y):
        def ID(self):
            return (self.x, self.y)

    def move(self, x, y):
        if (x, y) not in self.states:
            self.states[(x, y)] = self.State(x, y)
        self.state = self.states[(x, y)]
        if self.state.ID() in self.environment.rewards:
            reward = self.environment.rewards[self.state.ID()]
            self.state.estimatedValue = reward[0]
            if len(reward) > 2:
                self.move(reward[1], reward[2])
        else:
            self.state.estimatedValue = self.estimate()

    def chooseAction(self):
        action = self.actions[random.randint(0, 3)]
        self.move(self.state.x + action[0], self.state.y + action[1])

    def getEstimate(self, state, depth):
        if depth < 1:
            return state.estimatedValue
        # This is the reward for our math from formula 3.14
        estimate = self.environment.grid[state.y][state.x]
        # For each action that can be taken from the current state
        # Make an ID for that new state. This will be used to see
        # If the agent has information about that state.
        for action in self.actions:
            actionID = (state.x + action[0], state.y + action[1])
            if actionID not in self.states:
                continue
            statep = self.states[actionID]
            reward = self.environment.grid[statep.y][statep.x]
            # Policy value Estimate for a state is equal to the reward for the state plus
            # for each each possible state (statePrime) resulting from each action
            # their reward + discount Rate * state prime's estimated value
            # multiplied by the probability this action is taken
            estimate += 0.25 * (reward + self.getEstimate(statep, depth-1) * DISCOUNT)
        return estimate

    def estimate(self):
        return self.getEstimate(self.state, DEPTH)

    def printPolicy(self):
        for row in range(1, 6):
            gridrow = ""
            for cell in range(1, 6):
                stateID = (cell, row)
                num = 0
                if stateID in self.states:
                    num = self.states[stateID].estimatedValue
                if num >= 0:
                    gridrow += " "
                if num < 10:
                    gridrow += " "
                gridrow += "{:.1f}".format(num) + " | "
            print(gridrow[:-3])

class Environment:
    def __init__(self, size):
        self.rewards = {}
        fsize = size + 2
        self.grid = [
            [0 for i in range(fsize)] for j in range(fsize)
        ]
        for i in range(fsize):
            self.setReward(0, i, -1, 1, i)
            self.setReward(size+1, i, -1, size, i)
        for i in range(fsize):
            self.setReward(i, 0, -1, i, 1)
            self.setReward(i, size+1, -1, i, size)
    def setReward(self, x, y, value, xp, yp):
        self.rewards[(x, y)] = (value, xp, yp)
        self.grid[y][x] = value
    def getReward(self, x, y):
        return self.rewards[(x, y)]

env = Environment(SIZE)
env.setReward(x=2, y=1, value=10, xp=2, yp=5)
env.setReward(x=4, y=1, value=5, xp=4, yp=3)
agent = Agent(env)
for i in range(1000):
    agent.chooseAction()
agent.printPolicy()
