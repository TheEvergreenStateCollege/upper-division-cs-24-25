#!/bin/python3
import random

SIZE     = 4   # Size of movable area
DEPTH    = 3
EPSILON  = 0.1
DISCOUNT = 0.9 # Discount per square

class Agent:
    def __init__(self, environment):
        randx = random.randint(1, 4)
        randy = random.randint(1, 4)
        self.state = self.State(randx, randy)
        self.actions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.states = {}
        self.states[self.state.ID()] = self.state
        self.episodes = []
        self.currentEpisode = [[randx, randy]]
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
        self.currentEpisode.append([x, y])
        if (x, y) not in self.states:
            self.states[(x, y)] = self.State(x, y)
        self.state = self.states[(x, y)]
        if (x, y) in self.environment.rewards:
            reward = self.environment.getReward(x, y)
            if reward[0] == 0:
                self.newEpisode()
            if len(reward) > 2:
                self.move(reward[1], reward[2])
            return
        self.state.estimatedValue = self.getEstimate()

    def chooseAction(self):
        if random.random() > EPSILON:
            best = -1
            bestval = -9999
            action = None
            for i, a in enumerate(self.actions):
                actionID = (self.state.x + a[0], self.state.y + a[1])
                if actionID not in self.states:
                    continue
                val = self.states[actionID].estimatedValue
                if val > bestval:
                    best = i
                    bestval = val
            if best > -1:
                action = self.actions[best]
            else:
                action = self.actions[random.randint(0, 3)]
            self.move(self.state.x + action[0], self.state.y + action[1])
        else:
            action = self.actions[random.randint(0, 3)]
            self.move(self.state.x + action[0], self.state.y + action[1])

    def getEstimate(self):
        # This is the reward for our math from formula 3.14
        estimate = self.environment.grid[self.state.y][self.state.x]
        # For each action that can be taken from the current state
        # Make an ID for that new state. This will be used to see
        # If the agent has information about that state.
        for action in self.actions:
            actionID = (self.state.x + action[0], self.state.y + action[1])
            if actionID in self.states:
                statePrime = self.states[actionID]
                reward = self.environment.grid[statePrime.y][statePrime.x]
                # Policy value Estimate for a state is equal to the reward for the state plus
                # for each each possible state (statePrime) resulting from each action
                # their reward + discount Rate * state prime's estimated value
                # multiplied by the probability this action is taken
                estimate += 0.25 * (reward + statePrime.estimatedValue * DISCOUNT)
        return estimate

    def printPolicy(self):
        for row in range(1, SIZE+1):
            gridrow = ""
            for cell in range(1, SIZE+1):
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

    def newEpisode(self):
        print(self.currentEpisode)
        self.episodes.append(self.currentEpisode)
        randx = random.randint(1,4)
        randy = random.randint(1,4)
        self.state = self.State(randx, randy)
        self.currentEpisode = [[randx, randy]]

class Environment:
    def setReward(self, x, y, value, xprime=None, yprime=None):
        if xprime and yprime:
            self.rewards[(x, y)] = [value, xprime, yprime]
        else:
            self.rewards[(x, y)] = [value]
        self.grid[y][x] = value
    def getReward(self, x, y):
        return self.rewards[(x, y)]
    def __init__(self, size):
        self.rewards = {}
        fsize = size + 2
        self.grid = [
            [-1 for i in range(fsize)] for j in range(fsize)
        ]
        for i in range(fsize):
            self.setReward(0, i, -1, 1, i)
            self.setReward(size+1, i, -1, size, i)
        for i in range(fsize):
            self.setReward(i, 0, -1, i, 1)
            self.setReward(i, size+1, -1, i, size)

environment = Environment(SIZE)
environment.setReward(1, 1, 0)
environment.setReward(4, 4, 0)
agent = Agent(environment)
for i in range(1000):
    agent.chooseAction()
agent.printPolicy()
