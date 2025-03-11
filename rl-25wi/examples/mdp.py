#!/usr/bin/env python3

from abc import ABC, abstractmethod
from collections.abc import KeysView, Mapping, ValuesView
from dataclasses import dataclass
from functools import cache, reduce
from itertools import accumulate, product, repeat
from numbers import Number, Real
import operator
from random import choices
from typing import (
    Any, Callable, Dict, Iterator, List, FrozenSet, NewType, Self, 
    Sequence, Tuple, Union
    )
    
"""A module of utility classes/methods for representing MDPs."""

__author__ = "Joe Granville"
__date__ = "20250126"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"
  
class MDPException(Exception):
  pass

class MDPKeyError(MDPException, KeyError):
  pass

class MDPNotImplementedError(MDPException, NotImplementedError):
  pass

class FrozenMap[K, V](Mapping):
  """A hashable dict-like collection."""
  def __init__(
    self, 
    arg: Mapping[K, V] | None = None, 
    **kwargs: List[Tuple[K, V]]
  ) -> None:
    if isinstance(arg, Mapping):
      pairs = arg
    else:
      pairs = kwargs
    
    self.pairs = frozenset(pairs.items())
    
    return None
  
  def keys(self) -> KeysView[K]:
    return dict(list(self.pairs)).keys()
    
  @cache
  def domain(self) -> FrozenSet[K]:
    return frozenset(self.keys())
    
  def values(self) -> ValuesView[V]:
    return dict(list(self.pairs)).values()
  
  @cache
  def codomain(self) -> FrozenSet[V]:
    return frozenset(self.values())
  
  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, FrozenMap):
      return False
    return self.pairs == other.pairs
  
  def __hash__(self) -> int:
    return hash(self.pairs)
    
  @cache
  def __getitem__(self, key: Any) -> V:
    try:
      value = next(v for k, v in self.pairs if k == key)
    except StopIteration as e:
      raise CustomKeyError from e
    return value
  
  def __iter__(self) -> Tuple[K, V]:
    return iter(k for k, _ in self.pairs)
  
  @cache
  def __len__(self) -> int:
    return len(self.pairs)
    
  @cache
  def __repr__(self) -> str:
    return f'FrozenMap({dict(self.pairs)})'
    
  @staticmethod
  def freezeimage(
    domain: Sequence[K], 
    valuemap: Callable[K, V] | Mapping[K, V]
  ) -> Self:
    if isinstance(valuemap, Mapping):
      get_ = valuemap.get
    else:
      get_ = valuemap
    
    pairs = {key: get_(key) for key in domain}
    
    return FrozenMap(pairs)

  @staticmethod
  def uniquekeys(pairs: Sequence[Tuple[K, V]]) -> List[Tuple[K, V]]:
    ks = set(k for k, _ in pairs)
    uniquekeypairs = {}
    for key in ks:
      for k, v in pairs:
        if k == key:
          uniquekeypairs[k] = v
          break
    return uniquekeypairs

class FiniteDistribution[T](Mapping):
  """Represents a probability distribution over a set of type T.
  
  Does not have well-defined comparison; distributions with the same 
  normalized weights may have non-equal hashes. Comparisons should work 
  for mappings that are already normalized.
  """
  def __init__(
    self, 
    domain: Sequence[T], 
    mapping: Mapping[T, Real]
  ) -> None:
    self.domain = frozenset(domain)
    self.mapping = FrozenMap(mapping)
    return None
  
  def keys(self) -> KeysView[T]:
    return dict.fromkeys(domain, []).keys()
    
  @cache
  def domain(self) -> FrozenSet[T]:
    return frozenset(self.keys())
    
  def values(self) -> ValuesView[Real]:
    return self.normweights.values()
  
  @cache
  def codomain(self) -> FrozenSet[Real]:
    return frozenset(self.values())
    
  def __call__(self) -> T:
    return self.choose()
  
  def __eq__(self, other) -> bool:
    if not isinstance(other, FiniteDistribution):
      return False
    domaineq = self.domain == other.domain
    mappingeq = self.mapping == other.mapping
    return domaineq and mappingeq
  
  def __hash__(self) -> int:
    return hash((self.domain, self.mapping))
    
  @cache
  def __getitem__(self, key: Any) -> Real:
    if key not in self.domain:
      raise CustomKeyError
    else:
      return self.p(key)
  
  def __iter__(self) -> Iterator[T]:
    return iter(var for var in self.domain)
  
  @cache
  def __len__(self) -> int:
    return len(self.domain)
    
  @cache
  def __repr__(self) -> str:
    domain = self.domain
    mapping = self.mapping
    attributes = f'domain={domain}, mapping={mapping}'
    return f'FiniteDistribution({attributes})'
  
  def choose(self) -> T:
    return choices(list(self.domain), cum_weights=self.weights)
    
  @property
  @cache
  def normweights(self) -> FrozenMap[T, Real]:
    domain = list(self.domain)
    map_ = self.mapping
    maxweight = self.weights[-1]
    normweights = [map_[var] / maxweight for var in domain]
    return FrozenMap(dict(zip(domain, normweights)))
    
  @cache
  def p(self, var: T) -> Real:
    return self.normweights[var]
  
  @property
  @cache
  def weights(self) -> List[Real]:
    domain = list(self.domain)
    map_ = self.mapping
    weights = [map_[var] if var in map_ else 0.0 for var in domain]
    return tuple(accumulate(weights))
  
  @staticmethod
  def linear(
    domain: FrozenSet[T]
  ) -> Self:
    mapping = FrozenMap({var: 1.0 for var in domain})
    return FiniteDistribution(domain, mapping)
    
  @staticmethod
  def normalized(
    domain: FrozenSet[T], 
    mapping: FrozenMap[T, Real]
  ) -> Self:
    distribution = FiniteDistribution(domain, mapping)
    return FiniteDistribution(domain, distribution.normweights())
    
  @staticmethod
  def mixture(
    distributions: FrozenMap[Self, Real]
  ) -> Self:
    domain = set()
    mix = {}
    for dist, distw in distributions:
      domain = domain | dist.domain
      for var, varw in dist:
        mix[var] = mix.get(var, 0.0) + varw * distw
    return FiniteDistribution(domain, mix)

class MDP[S, A](ABC):

  @property
  @abstractmethod
  def curlyA_s(self) -> FrozenMap[S, FrozenSet[A]]:
    raise MDPNotImplementedError

@dataclass(frozen=True)
class TabularMDP[S, A](MDP):

  curlyS: FrozenSet[S]
  terminalS: FrozenSet[S]
  curlyA: FrozenSet[A]
  curlyR: FrozenSet[Real]
  bigPmap: FrozenMap[Tuple[S, A], FiniteDistribution[S]]
  bigRmap: FrozenMap[Tuple[S, A, S], FiniteDistribution[Real]]
    
  def bigP(self, s: S, a: A) -> FiniteDistribution[S]:
    return bigPmap[s, a]
    
  def bigR(self, s: S, a: A, sprime: S) -> FiniteDistribution[Real]:
    return bigRmap[s, a, sprime]
  
  def step(self, state: S, action: A) -> Tuple[S, Real]:
    newstate = bigP(state, action)()
    reward = bigR(state, action, new_state)()
    return newstate, reward
    
  @property
  @cache
  def curlySplus(self) -> FrozenSet[S]:
    return self.curlyS | self.terminalS
  
  @property
  @cache 
  def curlyA_s(self) -> FrozenMap[S, FrozenSet[A]]:
    as_ = {s: set() for s in self.curlyS}
    for s, a in self.bigPmap:
      as_[s].add(a)
    return FrozenMap({s: frozenset(as_[s]) for s in as_})
  
  def __call__(self, state: S, action: A) -> Tuple[S, Real]:
    return self.step(state, action)
    
def emptyQactions[S, A](
  mdpstruct: MDP[S, A], 
  default: Real = 0.0
) -> Dict[Tuple[S, A], Real]:
  return {pair: default for pair in mdpstruct.big_P}
  
def emptyQstates[S, A](
  mdpstruct: MDP[S, A], 
  default: Real = 0.0
) -> Dict[Tuple[S], Real]:
  return {state: default for state in mdpstruct.curly_S_plus}
  
def greedybyaction[S, A](
  state: S,
  qvalues: Dict[Tuple[S, A], Real],
  mdpstruct: MDP[S, A]
):
  actions = mdpstruct.curlyA_s(state)
  pairs = [(state, action) for action in actions]
  _, greedyaction = max(pairs, key=q_values.get)
  return greedyaction
  
def greedybystate[S, A](
  state: S,
  qvalues: Dict[Tuple[S], Real],
  mdpstruct: MDP[S, A]
):
  actions = mdpstruct.curlyA_s(s)
  _values = {}
  for action in actions:
    pdistribution = mdpstruct.bigP[action]
    newstates = pdistribution.mapping
    weightedvalue = sum(p * qvalues.r[s] for s, p in newstates)
    _values[action] = weightedvalue
  return max(weightedvalue, key=weightedvalue.get)

def zerotuple(n: int):
  return tuple(repeat(0, n))
  
def gridstates(
  lengths: Sequence[int],
  offsets: Sequence[int] = []
) -> FrozenSet[Tuple[int]]:
  if (padlength := len(lengths) - len(offsets)) > 0:
    offsets = tuple(*offsets) + zerotuple(padlength)
  ranges = zip(offsets, lengths)
  endpoints = [(off, off + _len) for off, _len in ranges]
  axes = [list(range(*ends)) for ends in endpoints]
  return list(product(*axes))
  
def centeredgrid(
  facediagonals: Sequence[int],
  origin: Sequence[int] = []
) -> FrozenSet[Tuple[int]]:
  if (padlength := len(facediagonals) - len(origin)) > 0:
    origin = tuple(*origin) + zerotuple(padlength)
  ranges = zip(origin, facediagonals)
  lengths = tuple((2 * dist) + 1 for dist in facediagonals)
  offsets = tuple(off - _len for off, _len in ranges)
  return gridstates(lengths, offsets)
  
def neighbors(origin: Sequence[int]) -> FrozenSet[Tuple[int]]:
  facediagonals = tuple(1 for _ in origin)
  neighborhood = centeredgrid(facediagonals, origin)
  return neighborhood - {origin}

def orthogonalneighbors(
  origin: Sequence[int]
) -> FrozenSet[Tuple[int]]:
  neighborhood = []
  for i in range(len(origin)):
    up = list(origin)
    up[i] = up[i] + 1
    down = list(origin)
    down[i] = down[i] - 1
    neighborhood.append(tuple(up))
    neighborhood.append(tuple(down))
  return neighborhood
  
def bounds(
  gridset: FrozenSet[Tuple[int]], 
  diagonals: bool = True
) -> FrozenSet[Tuple[int]]:
  if diagonals:
    neighborfun = neighbors
  else:
    neighborfun = orthogonalneighbors
  boundaryset = []
  for inbound in gridset:
    for point in neighborfun(inbound):
      if point not in gridset:
        boundaryset.append(point)
  return boundaryset
  
def vectoraddition(
  a: Sequence[Number], 
  b: Sequence[Number]
) -> Tuple[Number]:
  return tuple(n + m for n, m in zip(a, b))

DIRECTIONS = [
    ('right', 'left'), 
    ('up', 'down'), 
    ('in', 'out'), 
    ('before', 'after')
]

def labelunitorthogonals(
  n: int, 
  labels: Sequence[Sequence[str]] = DIRECTIONS
):
  origin = zerotuple(n)
  orthovectors = orthogonalneighbors(origin)
  # Sequence[1::2] means start at index 1 and take every 2nd item after
  oppositepairs = list(zip(orthovectors[::2], orthovectors[1::2]))
  ortholabelmap = {}
  # Normally we'd prefer zip to explicitly iterate the lists rather 
  # than using an index value to find the elements indirectly, but we 
  # have an extra use for i - generating labels procedurally
  for i in range(n):
    up, down = oppositepairs[i]
    if i < len(labels):
      ulabel, dlabel = labels[i]
    else:
      ulabel = 'd' + f'{i:0{n}}' + 'plus'
      dlabel = 'd' + f'{i:0{n}}' + 'minus'
    ortholabelmap[up] = ulabel
    ortholabelmap[down] = dlabel
  return ortholabelmap

def bresenham(dx, dy):
  """Modified Bresenham algorithm for points along a line from origin.
  
  Because the use case is collision detection, I've added partial 
  intersections to the results, where a segment in the iteration 
  intersects but does not end in a square.
  """
  match dx, dy:
    case 0, 0:
      return [(0, 0)]
    case _, 0:
      return [(x + 1, 0) for y in range(dx)]
    case 0, _:
      return [(0, y + 1) for x in range(dy)]

  negative_direction = dx < 0
  if negative_direction:
    dx = abs(dx)
  
  negative_slope = dy < 0
  if negative_slope:
    dy = abs(dy)
  
  slope_over_one = dx < dy
  if slope_over_one:
    i, j = dy, dx
  else:
    i, j = dx, dy

  # The grid is in the integers, so offset will represent the 
  # fractional portion of the x component. All the relevant expressions 
  # can be simplified to modulo arthmetic by multiplying by a factor of 
  # i
  offset = j - i
  x = 0
  trajectory = [(0, 0)]

  """
  # (0, 0) will be skipped in the iteration below, so hand-check the 
  # corner adjacencies
  if offset == 0:
    trajectory.append((x, 1))
  offset += j
  if offset >= 0:
    x = x + 1
    offset = offset - i
    trajectory.append((x, 0))
  """
  
  print(offset)
  for y in range(1, i + 1):
    print((x, y))
    trajectory.append((x, y)) # Mark where a step ends
    # If the offset is mod 0, the slope i/j must be 1, and we've 
    # crossed not just a y edge but a vertex
    # if offset == 0:
    #   trajectory.append((x, y + 1)) # Add the x neighbor
    offset = offset + j # Increment the fractional component of x
    print(offset)
    if offset >= 0: # Crossed an x edge
      x = x + 1 # Increment the whole by 1 (i mod i)
      print('edge')
      offset = offset - i # Subtract the same from the offset in modulo
      print(offset)
      trajectory.append((x, y)) # Add the y neighbor
      print((x, y))

  # trajectory.append((i, j))

  if not slope_over_one:
    trajectory = [(x, y) for y, x in trajectory]
  
  if negative_slope:
    trajectory = [(x, 0 - y) for x, y in trajectory]
  
  if negative_direction:
    trajectory = [(0 - x, y) for x, y in trajectory]
    
  return trajectory
  
def vectorsubtraction(
  a: Sequence[Number], 
  b: Sequence[Number]
) -> Tuple[Number]:
  return tuple(n - m for n, m in zip(a, b))
  
def vectorscalarmultiplication(
  a: Sequence[Number], 
  b: Number
) -> Tuple[Number]:
  return tuple(n * b for n in a)
  
"""To do:
- Wrap basic constructors with validators
"""