#!/bin/python3
from dataclasses import dataclass, astuple
import random

# Group:
# Shawn Bird
# Austin Strayer
# Hayden Edge

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
    # Return a random action if exploration triggers
    if random.random() < exploration or astuple(state) not in policy:
        return random.choice(list(actions.values()))
    # Find the highest valued action from the policy estimates for state
    highest = max(policy[astuple(state)], key=lambda x: x[1])[1]
    # Select randomly in case of a tie
    action, estimate = random.choice([x for x in policy[astuple(state)] if x[1] == highest])
    # Choose randomly from all actions if no good estimate found
    if estimate <= 0:
        return random.choice(list(actions.values()))
    return action

def estimateValue(stateTup, action, newStateTup, reward):
    if stateTup not in policy:
        policy[stateTup] = []
    # Get index of action from policy
    try:
        index = [a[0] for a in policy[stateTup]].index(action)
    except ValueError:
        index = len(policy[stateTup])
        policy[stateTup].append((action, reward))
    estimate = policy[stateTup][index][1]
    # Get the highest estimate from the next state
    try:
        outcome = max(policy[newStateTup], key=lambda x: x[1])[1]
    except KeyError:
        outcome = 0
    # Use Tabular Q Learning to update the policy estimate
    estimate += stepsize * (reward + discount * outcome - estimate)
    policy[stateTup][index] = (action, estimate)

def takeAction(state, action):
    newState, reward = env.resolveAction(state, action)
    # Record the action if it results in a state change
    if newState is not state:
        estimateValue(astuple(state), action, astuple(newState), reward)
        model[(astuple(state), action)] = (astuple(newState), reward)
    return newState

def modelAction(state, action):
    newState, reward = model[(state, action)]
    estimateValue(state, action, newState, reward)
    return newState

def runMaze(state):
    episode = []
    while env.getReward(state.x, state.y) <= 0:
        action = chooseAction(state)
        episode.append((state, action))
        state = takeAction(state, action)
        modelState = state
        for _ in range(modeling):
            randState, randAction = random.choice(list(model.keys()))
            modelState = modelAction(randState, randAction)
    return episode

def drawGrid(env, state, action=None):
    line = ''
    char = 'S'
    if action:
        if action is actions["left"]:
            char = "←"
        elif action is actions["right"]:
            char = "→"
        elif action is actions["up"]:
            char = "↑"
        elif action is actions["down"]:
            char = "↓"
    for i, s in enumerate(env.grid):
        if s == WALL:
            line += 'X'
        elif i == env.getIndex(state.x, state.y):
            line += char
        elif s > 0:
            line += 'G'
        else:
            line += ' '
        line += ' '
        if (i + 1) % env.width == 0:
            print(line)
            line = ''
    print(line)

# Set initial variables
exploration = 0.1
stepsize = 0.1
discount = 0.95
modeling = 5
env = Environment(width=11, height=8)

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

# Example: policy[astuple(state)] = [(actions["up"], estimate)]
policy = {}  # k = state tuple, v = [(action, estimate)]
model = {}  # k = (state tuple, action), v = (next state tuple, reward)
# Actions: "name": (x change, y change)
actions = {"up": (0, -1), "right": (1, 0), "down": (0, 1), "left": (-1, 0)}

# Run maze until optimal
optimal = 14 # Minimum moves from start to reward
episodes = []
while True:
    episode = runMaze(start)
    episodes.append(episode)
    if len(episode) <= optimal:
        break

# Print last run along with stats
for step in episodes[-1]:
    drawGrid(env, step[0], step[1])
print(len(episodes[-1]), "moves")
print(len(episodes), "episodes")
