#!/usr/bin/env python3

from mdp import (
    bresenham, FiniteDistribution, FrozenMap, gridstates, 
    labelunitorthogonals, MDP, orthogonalneighbors, vectoraddition, 
    zerotuple
    )
    
"""A module implementing labs 6 and 7 (windy gridworld).

Taken from example 6.5 (Sutton & Barto p130).
"""

__author__ = "Joe Granville"
__date__ = "20250213"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

DIMENSION = 2
ROWS = 7
COLUMNS = 10
STARTING_POSITION = (3, 0)
GOAL_POSITION = (3, 7)
WIND_COLUMNS = {3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 1}
for n in range(COLUMNS):
  if not n in WIND_COLUMNS:
    WIND_COLUMNS[n] = 0

class Lab6Exception(Exception):
  pass
  
class Lab6TypeError(Lab6Exception, TypeError):
  pass
  
class Lab6NotImplementedError(Lab6Exception, NotImplementedError):
  pass

ORIGIN_TUPLE = zerotuple(DIMENSION)

GRID_PAIRS = frozenset(gridstates((ROWS, COLUMNS), ORIGIN_TUPLE))
MOVE_PAIRS = frozenset(orthogonalneighbors(ORIGIN_TUPLE))
MOVE_LABELS = labelunitorthogonals(DIMENSION)

class Point2D(tuple):
  def __new__(cls, x, y):
    return super().__new__(cls, (x, y))

class Action(Point2D):
  def __str__(self):
    return MOVE_LABELS[self] if self in MOVE_LABELS else str(self)
      
CURLY_A = frozenset(Action(x, y) for x, y in MOVE_PAIRS)
    
class State(Point2D):
  def __add__(self, other):
    if not isinstance(other, Action):
      errstr = "Expected an Action for 'other' argument"
      raise Lab6NotImplementedError(errstr)
    return State(*vectoraddition(self, other))
    
NONTERMINAL_PAIRS = GRID_PAIRS - {GOAL_POSITION}
CURLY_S = frozenset(State(x, y) for x, y in NONTERMINAL_PAIRS)
GOAL = State(*GOAL_POSITION)
TERMINAL_S = frozenset({GOAL})

def bresenham2d(v):
  ...

def boundcollision(a, b, inbounds):
  ...

def windygridtransitions(curlyS, curlyA, wind):
  bigP = {}
  for s, a in zip(CURLY_S, CURLY_A):
    windforce = Action(0, wind[s])
    resultingmove = s + a + windforce
    bigP[s, a] = FiniteDistribution.linear([resultingmove])
  return bigP
  
def fixedepisodicrewards(reward, bigP):
  bigR = {}
  for (s, a), sps in bigP.items():
    for s_ in sps:
      bigR[s, a, s_] = reward
  return bigR


  