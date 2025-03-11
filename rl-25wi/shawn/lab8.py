#!/bin/python3
from dataclasses import dataclass, astuple
import random

# Group:
# Shawn Bird
# Austin Strayer

## Goals: understand Dyna-Q and planning
## Task: program the Dyna-maze (P.164)  in Python, where the model and the
## environment are distinct. The model estimates the reward and next state
## based on previous experience.
## 1. build the environment/grid. The environment needs to implement a
##    function with the spec
##    - input: state-action pair
##    - output: state, reward
## 2. The model also needs implement a similar function
## 3. build a simple agent: choose an action
## 4. build the simulation based on the model. The simulation only samples
##    states that have been already visited.
## Work in groups and make sure  include the names of the members in your group

# Use negative infinity to represent a wall tile
WALL = float('-inf')

class Environment:
    def __init__(self, width=12, height=12):
        self.width = width
        self.height = height
        self.grid = [0.0 for _ in range(width * height)]

    # Index 1d array as 2d coordinates
    def getIndex(self, x, y) -> int:
        return self.width * y + x

    def getReward(self, x, y):
        return self.grid[self.getIndex(x, y)]

    def setReward(self, x, y, value):
        self.grid[self.getIndex(x, y)] = value

    def resolveAction(self, state, action) -> tuple:
        newState = State(state.x + action[0], state.y + action[1])
        reward = self.getReward(newState.x, newState.y)
        # Hitting a wall
        if reward == WALL:
            return (state, 0)
        return (newState, reward)


@dataclass
class State:
    x: int
    y: int


def chooseAction(state):
    # Return a random action if epsilon triggers
    if random.random() < epsilon or astuple(state) not in policy:
        return random.choice(list(actions.values()))
    # Return the highest valued action from the policy estimate
    action, estimate = max(policy[astuple(state)], key=lambda x: x[1])
    if estimate <= 0:
        return random.choice(list(actions.values()))
    return action


def takeAction(state, action):
    newState, reward = env.resolveAction(state, action)
    if astuple(state) not in policy:
        policy[astuple(state)] = []
    try:
        index = [a[0] for a in policy[astuple(state)]].index(action)
    except ValueError:
        index = len(policy[astuple(state)])
        policy[astuple(state)].append((action, reward))
    estimate = policy[astuple(state)][index][1]
    # TODO fix this
    try:
        outcome = max(policy[astuple(newState)], key=lambda x: x[1])[1]
    except KeyError:
        outcome = 0
    estimate += alpha * (reward + gamma * outcome - estimate)
    policy[astuple(state)][index] = (action, estimate)
    modelkey = (astuple(state), action)
    modelval = (reward, astuple(newState))
    if modelkey not in model:
        model[modelkey] = [modelval]
    elif modelval not in model[modelkey]:
        model[modelkey].append(modelval)
    return newState

def runMaze(state):
    episode = []
    while env.getReward(state.x, state.y) == 0:
        action = chooseAction(state)
        episode.append((state, action))
        state = takeAction(state, action)
        drawGrid(env, state)
    return episode

def drawGrid(env, state):
    line = ''
    for i, s in enumerate(env.grid):
        if s == WALL:
            line += 'X'
        elif i == env.getIndex(state.x, state.y):
            line += 'S'
        elif s > 0:
            line += 'G'
        else:
            line += ' '
        line += ' '
        if (i + 1) % env.width == 0:
            print(line)
            line = ''
    print(line)

epsilon = 0.1
alpha = 1
gamma = 0.9
env = Environment(11,8)

# Set walls around perimeter
for i, reward in enumerate(env.grid):
    mod = i % env.width
    if (
        mod == 0
        or mod == env.width - 1
        or i < env.width - 1
        or i > env.width * (env.height - 1)
    ):
        env.grid[i] = WALL

# Add inner walls
env.setReward(3,2, WALL)
env.setReward(3,3, WALL)
env.setReward(3,4, WALL)
env.setReward(6,5, WALL)
env.setReward(8,1, WALL)
env.setReward(8,2, WALL)
env.setReward(8,3, WALL)

# Place goal
env.setReward(9,1, 1)

# Set starting position and draw grid
start = State(1, 3)
drawGrid(env, start)

# example: policy[astuple(state)] = [(actions["up"], estimate)]
policy = {}  # k = state tuple, v = [action, estimate]
model = {}  # k = state tuple, v = [reward, next state tuple]
actions = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}

episodes = []
for _ in range(10):
    episode = runMaze(start)
    episodes.append(episode)
    print(len(episode), "moves")

#print(policy)
