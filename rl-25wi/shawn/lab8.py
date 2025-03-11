#!/bin/python3
from dataclasses import dataclass, astuple

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

    # Index 1d array as 2d coords
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
    # Return the highest valued action from the policy eval
    action, _ = max(policy[astuple(state)], key=lambda x: x[1])
    # random.choice(list(actions.values()))
    return action


def takeAction(state, action):
    newState = env.resolveAction(state, action)
    return newState


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
env.setReward(9,1, 5)

line = ''
for i, s in enumerate(env.grid):
    if s == WALL:
        line += 'X'
    elif s > 0:
        line += 'G'
    else:
        line += ' '
    line += ' '
    if (i + 1) % env.width == 0:
        print(line)
        line = ''
print(line)

# example: policy[astuple(state)] = [(actions["up"], estimate)]
policy = {}  # k = state, v = [action, estimate]
actions = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}
episodes = []
start = State(1, 3)
