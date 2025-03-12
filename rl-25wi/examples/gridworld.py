#!/usr/bin/env python3

from itertools import islice, product
from random import choice

"""A no-frills implementation of example 3.5 (Sutton & Barto p80)."""

__author__ = "Joe Granville"
__date__ = "20250124"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

SCALE = 5

CURLY_S = list(product(range(1, SCALE + 1), range(1, SCALE + 1)))

GOALS = {
  (2, 5): {'moveto': (2, 1), 'reward': 10.0, 'label': 'A'},
  (4, 5): {'moveto': (4, 3), 'reward': 5.0, 'label': 'B'}
}
  
CURLY_A = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def pirandom(state):
  return choice(CURLY_A)

def addtuples(a, b):
  return tuple(n + m for n, m in zip(a, b))

def gridworld(state, action):
  newstate = addtuples(state, action)
  
  if newstate not in CURLY_S:
    return state, -1.0
  
  if newstate in GOALS.keys():
    goalarc = GOALS[newstate]
    print(f"Arrived at goal {goalarc['label']}")
    return goalarc['moveto'], goalarc['reward']
  else:
    return newstate, 0.0
  
def randomstart():
  return choice(CURLY_S)
  
def emptyQ():
  return {s: (0.0, 0) for s in CURLY_S}
  
def updateQ(big_Q, state, action, reward):
  reachedstate = add_tuples(state, action)
  
  if reachedstate not in CURLY_S:
    reachedstate = state
    
  total, visitcount = bigQ[reached_state]
  bigQ[reachedstate] = (total + reward, visitcount + 1)
  
  return bigQ
    
def episode(
    bigQ={}, 
    pi=pirandom, 
    environment=gridworld, 
    initial_s=randomstart
):
  if len(bigQ) is not len(CURLY_S):
    bigQ = emptyQ()
    
  state = initial_s()
  
  while True:
    action = pi(state)
    newstate, reward = environment(state, action)
    updateQ(bigQ, state, action, reward)
    yield state, action, newstate, reward, bigQ
    state = newstate
  
if __name__ == '__main__':
  print(islice(episode(), 1000))
  