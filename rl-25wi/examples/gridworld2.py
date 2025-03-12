#!/usr/bin/env python3

from itertools import batched, islice, product
from random import choice, random

"""A no-frills implementation of example 3.5 (Sutton & Barto p80).

OK, some frills: a pretty printer and an epsilon-greedy policy based on 
the value estimate.

This implementation is data-driven; the behavior is largely determined  
by stored values.

This implementation is also reified. Reification is a design strategy 
where the features of the problem domain are made "real" in the code 
environment.

As much as I could manage, the organization and structure is aligned 
with the conceptual definitions of reinforcement learning. When I have 
to adapt an idea to "how Python does it", I do my best to encapsulate 
that within a single function/class, and then present a mathematically 
consistent interface on the outside.

Related concepts include abstraction, encapsulation, loose coupling, 
invariants, design-by-contract, domain-driven design and 
responsibility-driven design.
"""

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
  
def updateQ(state, action,  _, reward, bigQ, _):
  reachedstate = addtuples(state, action)
  
  if reachedstate not in CURLY_S:
    reachedstate = state
    
  total, visitcount = bigQ[reached_state]
  bigQ[reachedstate] = (total + reward, visitcount + 1)
  
  return None
    
def episode(
    big_Q={}, 
    pi=pirandom, 
    environment=gridworld, 
    initial_s=randomstart,
    stepcallback=updateQ
):
  if len(bigQ) is not len(CURLY_S):
    bigQ = emptyQ()
    
  state = initial_s()
  
  step = 0
  
  while True:
    action = pi(state)
    newstate, reward = environment(state, action)
    
    if stepcallback is not None:
      stepcallback(state, action, newstate, reward, bigQ, step)
    
    yield state, action, newstate, reward, bigQ, step
    state = newstate
    step = step + 1
  
def maximalaction(bigQ, state):
  neighbors = {}
  
  for action in CURLY_A:
    neighborstate = addtuples(state, action)
    if neighborstate in CURLY_S:
      neighbors[action] = bigQ[neighborstate]
      
  maxQ = max(neighbors.values())
  maxA = [action for action, value in neighbors if value == maxQ]
  
  return choice(maxA)

def piepsilongreedy(bigQ, epsilon=0.01):
  def pi(state):
    if random() > epsilon:
      return choice(maximalaction(bigQ, state))
    else:
      return choice(CURLY_A)
  return pi
  
def randomstart_withoutgoals():
  starts = [state for state in CURLY_S if state not in GOALS.keys()]
  return choice(starts)
  
def average(sum_, count_):
  if count_ == 0:
    return 0.0
  else:
    return sum_ / count_

def pprintstep(state, action, newstate, reward, step):
  print(f'Step {step}: {state}, {action} -> {newstate}, {reward}')
  return None

def qvaluestostrings(bigQ):
  qvalues = [bigQ[state] for state in sorted(bigQ)]
  qvaluefloats = [average(vsum, vcount) for vsum, vcount in qvalues]
  qvaluestrings = [f'{vfloat:8.1f}' for vfloat in qvaluefloats]
  qvaluegrid = list(batched(qvaluestrings, SCALE))
  qvaluelines = [' '.join(vstrings) for vstrings in qvaluegrid]
  return qvaluelines
  
def pprintvalues(_, _, _, _, bigQ, step):
  qvaluelines = qvaluestostrings(bigQ)
  tablewidth = len(qvaluelines[0])
  print('Q: '.rjust(tablewidth, '-'))
  print(*qvaluelines, sep='\n')
  print(f' step: {step:<6} '.ljust(tablewidth, '-'))
  return None

def pprintupdate(state, action, newstate, reward, bigQ, step):
  updateQ(state, action, newstate, reward, bigQ, step)
  pprintstep(state, action, newstate, reward, step)
  pprintvalues(state, action, newstate, reward, bigQ, step)
  return None

def pprintevery(n):
  def updatefun(state, action, newstate, reward, bigQ, step):
    updateQ(state, action, newstate, reward, bigQ, step)
    pprintstep(state, action, newstate, reward, step)
    if step % n == 0:
      pprintvalues(state, action, newstate, reward, bigQ, step)
    return None
  return updatefun

if __name__ == '__main__':
  print(islice(episode(stepcallback=pprintevery(10)), 1000))
  