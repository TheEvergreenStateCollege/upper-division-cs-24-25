#!/usr/bin/env python3

from collections import namedtuple
from contextlib import contextmanager
from itertools import product
from random import choice, choices, random
    
"""A module implementing lab 8 (Dyna-Q maze).

Taken from example 8.1 (Sutton & Barto p164).

I wrote this by carefully reading the pseudocode for tabular Dyna-Q and 
implementing each mathematical object it mentions, independent of the 
overall algorithm.

As a result, it should be relatively easy to extend this to Dyna-Q+, as 
all the constituent parts are reusable - the only things that remain
are to record recency and add an additional term to the reward signal 
in the q-value updates.

But also the types, constants and functions I needed are all 
interleaved, and not ordered in a way that would be practical for a 
real application with a long-term development lifecycle. So don't use 
this as a model for tidiness.

It runs alright but I'm not convinced it's correct.
"""

__author__ = "Joe Granville"
__date__ = "20250306"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

XYPoint = namedtuple('XYPoint', ('x', 'y'))

State = type('State', (XYPoint,), {})
St = State

GOAL = St(8, 5)
START = St(0, 4)

WALL_1 = frozenset((St(2, 2), St(2, 3), St(2, 4)))
WALL_2 = frozenset((St(7, 3), St(7, 4), St(7, 5)))
WALLS = frozenset(WALL_1 | WALL_2 | {St(5, 1)})

X_SIZE, Y_SIZE = 8, 5
X_BOUNDS = range(X_SIZE + 1)
Y_BOUNDS = range(Y_SIZE + 1)
X_RANGE = range(-1, X_SIZE + 2)
Y_RANGE = range(-1, Y_SIZE + 2)
XY_PAIRS = frozenset(product(X_RANGE, Y_RANGE))
STATES = frozenset(St(x, y) for x, y in XY_PAIRS)
IN_BOUNDS_PAIRS = frozenset(product(X_BOUNDS, Y_BOUNDS))
IN_BOUNDS_STATES = frozenset(St(x, y) for x, y in IN_BOUNDS_PAIRS)

OUTER_WALL = frozenset(STATES - IN_BOUNDS_STATES)
TERMINAL_S = frozenset({GOAL})
BARRIERS = frozenset(WALLS | OUTER_WALL)
BIG_S = frozenset(STATES - (BARRIERS | TERMINAL_S))

Action = type('Action', (XYPoint,), {})
Ac = Action

ACTIONS = {
    'Right': Ac(1, 0),
    'Up': Ac(0, 1),
    'Left': Ac(-1, 0),
    'Down': Ac(0, -1)
    }
ACTION_STRS = list(ACTIONS.keys())

StateAction = namedtuple('StateAction', ('s', 'a'))
StAc = StateAction

SA_PAIRS = frozenset(product(STATES, ACTIONS))
STATEACTIONS = frozenset(StAc(s, a) for s, a in SA_PAIRS)

def pairs_at(state):
  return tuple(StAc(s, a) for s, a in product((state,), ACTIONS))

def makeqdict():
  return {sa: 0.0 for sa in STATEACTIONS}
  
def maxvalue_(state, q):
  return max(pairs_at(state), key=q.get)
  
def maxactions(state, q):
  maxvalue = q[max(pairs_at(state), key=q.get)]
  ismax = lambda sa: q[sa] == maxvalue
  pairs = tuple(filter(ismax, pairs_at(state)))
  maxactions_ = tuple(a for _, a in pairs)
  return maxactions_
  
ModelVal = namedtuple('ModelVal', ('r', 's_'))
MVal = ModelVal

def makemodeldict():
  # Surprise! Presence of a key in the model will be used to tell if a 
  #   pair has been visited before, so an empty dict is helpful here
  return {}
  
def visited(model):
  # Curly braces with single items and not pairs are a set
  uniquestates = {s for s, _ in model.keys()}
  return list(uniquestates)

EPSILON = 0.1

def egreedy(state, q, e=EPSILON):
  availableoptions = pairs_at(state)
  if random() > e:
    egreedyaction = choice(maxactions(state, q))
  else:
    egreedyaction = choice(ACTION_STRS)
  return egreedyaction

def validmove(newstate):
  return newstate not in BARRIERS

def bigP(state, action):
  s = state
  a = ACTIONS[action]
  s_ = St(s.x + a.x, s.y + a.y)
  if not validmove(s_):
    s_ = s
  return s_

def bigR(state, action, newstate):
  if newstate == GOAL:
    r = 1.0
  else:
    r = 0.0
  return r

def transition(state, action):
  newstate = bigP(state, action)
  if newstate == GOAL:
    nextstate = START
  else:
    nextstate = newstate
  return bigR(state, action, newstate), nextstate
  
ALPHA = 0.1
GAMMA = 0.95

SARTriple = namedtuple('SARTriple', ('s', 'a', 'r'))
STri = SARTriple

# Nesting a namedtuple is not great and suggests you might need a more
#   explicit and meaningful class definition
# But here I am doing it
Step = namedtuple('Step', ('sar', 'q', 'model'))

def tabdynaq(start, n, q=None, model=None, gamma=GAMMA, alpha=ALPHA):
  if q is None:
    q = makeqdict()
  if model is None:
    model = makemodeldict() # Item (a)
  
  s = start
  s_ = None # I don't know what this yet is but I need to name it now
  
  # gammaterm is a closure capturing q and s_ from an outer scope
  gammaterm = lambda : gamma * q[max(pairs_at(s_), key=q.get)]
  # alphaterm doesn't capture the outside s because it creates its own 
  #   instance variables in its own scope when it names an argument s
  alphaterm = lambda s, a, r: alpha * (r + gammaterm() - q[s, a])
  
  while True:
    a = egreedy(s, q) # Item (b)
    r, s_ = transition(s, a) # Item (c)
    q[s, a] = q[s, a] + alphaterm(s, a, r) # Item (d)
    model[s, a] = MVal(r, s_) # Item (e)
    sartriple = STri(s, a, r)
    nextstate = s_ # Save these before using them in the modeling loop
    for prev_s in choices(visited(model), k=n): # Item (f)
      s = prev_s # Item (f.1)
      prev_as = list(filter(lambda sa: sa in model, pairs_at(s)))
      a = choice(prev_as).a # Item (f.2)
      r, s_ = model[s, a] # Item (f.3)
      q[s, a] = q[s, a] + alphaterm(s, a, r) # Item (f.4)
    yield Step(sartriple, q, model) # The name adds a bit of meaning
    s = nextstate
    
"""The choice of which variables to capture was kind of arbitrary. I 
could capture them all rather than any parameter passing, or do all 
parameter passing.

It's good to favor passing parameters. Closures are very magical and 
not easy on the reader.

Here I thought five parameters was too much for alphaterm, so I decided 
to capture the two that were nested deepest/used the most. If I wanted 
to be really slick, I could wrap the whole q update in a single lambda 
and reuse it between (d) and (f.4).
"""

def dosteps(iterobj, n, visitorfun=None):
  if visitorfun is None:
    visitorfun = lambda _: None
  while True:
    print('dosteps(): Cooking...')
    for _ in range(n):
      step = next(iterobj)
      visitorfun(step)
    print(f'dosteps(): Did n={n} steps')
    print('dosteps(): Bon appétit')
    yield step

def reachedgoal(step):
  return step.sar.r == 1.0

def waitforgoal(iterobj, visitorfun=None):
  if visitorfun is None:
    visitorfun = lambda _: None
  n = 0
  print('waitforgoal(): Waiting...')
  while True:
    step = next(iterobj)
    visitorfun(step)
    n = n + 1
    if reachedgoal(step):
      print('waitforgoal(): Got it!')
      print(f'waitforgoal(): Hit the goal in n={n} iterations')
      yield step
      n = 0
      print('waitforgoal(): Waiting...')

def watchforgoals(step):
  if reachedgoal(step):
    print('watchforgoals(): GOOOAL!')
  return step

def printtriples(step):
  print(f'printtriples(): step.sar = {step.sar}')
  return step
  
def printcurrentq(step):
  s = step.sar.s
  a = step.sar.a
  print(f'printcurrentq(): step.q[s, a] = {step.q[s, a]}')
  return step

# This is far from the best way to do this
def doallthosethings(step):
  return watchforgoals(printtriples(printcurrentq(step)))
  
@contextmanager
def trivialcontextmanager():
  # Would set something up here
  print('trivialcontextmanager(): Entering a with block')
  yield 'an important resource like a file handle'
  # Would tear something down here
  print('trivialcontextmanager(): Exiting a with block')
  # I only made this to illustrate the with block
  return None
  
if __name__ == '__main__':
  with trivialcontextmanager() as something:
    print('''Inside a block these variables technically aren't global''')
    print('''Because they're inside a block, they disappear on exit''')
    dq = tabdynaq(START, 10)
    iterator = waitforgoal(dq, doallthosethings)
    iterator = dosteps(iterator, 100)
    # Find the goal five times and print a lot of stuff in the mean time
    nextstep = next(iterator)
    print('Results of training for one hundred goals:')
    print(nextstep)
    print(f'And all I got was this lousy "{something}"')
  print('Poof! No more example objects. Make your own.')