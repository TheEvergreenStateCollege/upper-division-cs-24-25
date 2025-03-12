#!/usr/bin/env python3

from itertools import chain, product, tee
from math import floor

from matplotlib import colormaps
from matplotlib.collections import PatchCollection
from matplotlib.colors import Colormap
from matplotlib.pyplot import (
    draw, ion, pause, show, subplots, xticks, yticks
    )
from matplotlib.path import Path
from matplotlib.patches import (
    FancyArrowPatch, Patch, PathPatch, Rectangle, RegularPolygon
    )

from lab8 import (
    ACTIONS, BARRIERS, bigP, BIG_S, doallthosethings, dosteps, 
    pairs_at, reachedgoal, SARTriple, START, Step, tabdynaq, 
    TERMINAL_S, waitforgoal, X_RANGE, Y_RANGE
    )
    
"""A matplotlib-based driver for lab8.py (Dyna-Q maze).

Based on example 8.1 (Sutton & Barto p164).

This uses a cheap trick for distributing the same step updates among 
many separate functions. If you like this, know that in real 
application this kind of behavioral composition is accomplished by 
things like event- or message-based architectures.

Deeply nesting generators is not a great choice for real-life designs 
that need to grow over time, so be ready to transition to stronger 
techniques as you learn more.

Not only is this a bad example of design - matplotlib is probably a 
bad choice in general for visualizing a high-speed algorithm.
"""

__author__ = "Joe Granville"
__date__ = "20250308"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

PAUSE_SECONDS = 0.001 # Chosen arbitrarily

X_LIMIT = (min(X_RANGE), max(X_RANGE))
Y_LIMIT = (min(Y_RANGE), max(Y_RANGE))
X_DELTA = abs(X_LIMIT[1] - X_LIMIT[0])
Y_DELTA = abs(Y_LIMIT[1] - Y_LIMIT[0])
# Taxicab distance is a nice "Platonic" measure of a path on a grid
TAXICAB_DIST = X_DELTA + Y_DELTA
DEF_THRESHHOLD = floor(TAXICAB_DIST / 2)
QPATCHSIZE = 0.3125
TILESIZE = 0.8375
TILEOFFSET = (0 - TILESIZE / 2, 0 - TILESIZE / 2)
WALLSIZE = 0.975
WALLOFFSET = (0 - WALLSIZE / 2, 0 - WALLSIZE / 2)
  
class ReversedColormap(Colormap):
  
  def __init__(self, cmap):
    self.cmap = cmap
    return None
    
  def __call__(self, val):
    return self.cmap(1.0 - val) # Colormaps are defined on range (0, 1]

CMAP_BLUES = colormaps['Blues']
CMAP_BLUES_REV = ReversedColormap(CMAP_BLUES)
CMAP_CIVIDIS = colormaps['cividis']
CMAP_CIVIDIS_REV = ReversedColormap(CMAP_CIVIDIS)
CMAP_GNUPLOT = colormaps['gnuplot']
CMAP_GNUPLOT_REV = ReversedColormap(CMAP_GNUPLOT)
CMAP_PRISM = colormaps['prism']
    
def pairwise(iterable):
  a, b = tee(iterable)
  next(b, None)
  return zip(a, b)

def createplot():
  fig, axes = subplots()
  ion() # Return contextlib.ExitStack?
  return fig, axes

def rectangle(point, size, **kwargs):
  return Rectangle(point, size, size, **kwargs)

def polygon(point, size, **kwargs):
  radius = size / 2
  if 'numVertices' not in kwargs:
    kwargs['numVertices'] = 4
  polygonpatch = RegularPolygon(
      point, radius=radius, **kwargs
      )
  return polygonpatch

def pathpatchesfrom(path, threshhold, midpoint=0.5, cmap=None):
  path_ = path
  if len(path) == 1:
    path_.append(path[0])
  threshhold_ = 0 - threshhold
  pairs = list(pairwise(path_))
  
  if cmap is None:
    cmap = CMAP_CIVIDIS
  
  headcmap = lambda i, n: cmap(midpoint + i * (1.0 - midpoint) / n)
  tailcmap = lambda i, n: cmap((i + 1) * midpoint / n)
  
  if threshhold > len(path):
    head = pairs
    tail = []
  else:
    head = pairs[threshhold_:]
    tail = pairs[:threshhold_]
  
  drawnparts = [(tail, tailcmap), (head, headcmap)]
  patchcollections = []
  for part, cmap_ in drawnparts:
    if part:
      nparts = len(part)
      patches = []
      for i, segment in enumerate(part):
        if segment[0] != segment[1]:
          pathpatch = PathPatch(
              Path(segment), edgecolor=cmap_(i, nparts), 
              facecolor='none', linewidth=3
              ) # Too many args, wish I could do something about this
          patches.append(pathpatch)
        nodepatch = polygon(
              segment[0], 0.15625, color=cmap_(i, nparts), 
              numVertices=12
              )
        patches.append(nodepatch)
      collection = PatchCollection(patches, match_original=True)
      patchcollections.append(collection)
  return patchcollections
  
def addpair(a, b):
  return a[0] + b[0], a[1] + b[1]

def patchesfrom(
  points, constructor, color=None, cmap=None, size=None, **kwargs
  ):
  if cmap is None:
    cmap = CMAP_PRISM
  if size is None:
    size = TILESIZE
  npoints = len(points)
  patches = []
  colors = []
  if color:
    colors = [color] * npoints
  else:
    colors = [cmap(i / npoints) for i in range(npoints)]
  for point, color_ in product(points, colors):
    patch = constructor(point, size, **kwargs)
    patch.set_facecolor(color_)
    patches.append(patch)
  return patches
  
WALLPOINTS = [addpair(point, WALLOFFSET) for point in BARRIERS]
def wallpatches():
  walls = patchesfrom(
      WALLPOINTS, rectangle, color='black', fill=True, linewidth=5, 
      size=WALLSIZE
      )
  return walls
  
STARTPOINTS = [addpair(START, TILEOFFSET)]
GOALPOINTS = [addpair(point, TILEOFFSET) for point in TERMINAL_S]
def specialtilepatches():
  start = patchesfrom(
      STARTPOINTS, rectangle, edgecolor=('green', 0.5), 
      facecolor='none', fill=False, linewidth=5
      )
  goals = patchesfrom(
      GOALPOINTS, rectangle, edgecolor=('red', 0.5), facecolor='none', 
      fill=False, linewidth=5
      )
  return start + goals
  
def currentstatepatch(step):
  state = addpair(step.sar.s, (0, 0))
  currentstate = patchesfrom(
      [state], polygon, color='black', size=0.3125, zorder=2
      )
  return currentstate

def mulpair(pair, n):
  return pair[0] * n, pair[1] * n

HALF_A = {a: mulpair(ACTIONS[a], 0.5) for a in ACTIONS}

def currentactionarrowpatch(step):
  state = step.sar.s
  action = addpair(state, HALF_A[step.sar.a])
  arrow = FancyArrowPatch(
      state, action, arrowstyle='fancy', color='red', 
      mutation_scale=20, zorder=3
      )
  return [arrow]

THREE_SIXTEENTHS_A = {a: mulpair(ACTIONS[a], 0.1875) for a in ACTIONS}
THREE_32NDS_A = {a: mulpair(ACTIONS[a], 0.09375) for a in ACTIONS}

def qvaluepatches(step, cmap=None):
  if cmap is None:
    cmap = CMAP_BLUES_REV
  patches = []
  qs = list(step.q.values())
  minq = min(qs)
  maxq = max(qs)
  if minq == maxq:
    d = 1
  else:
    d = maxq - minq
  for state in BIG_S:
    pairs = pairs_at(state)
    localqs = [step.q[sa] for sa in pairs]
    localmin = min(localqs)
    localmax = max(localqs)
    if localmin == localmax:
      locald = 1
    else:
      locald = localmax - localmin
    for sa in pairs:
      _, action = sa
      color = cmap(1.0 - ((step.q[sa] - minq) / (2 * d)))
      qpos = addpair(state, THREE_SIXTEENTHS_A[action])
      qvaluepatch = polygon(qpos, QPATCHSIZE, color=color, zorder=0)
      localcolor = cmap(1.0 - (step.q[sa] - localmin) / locald)
      localpos = addpair(state, THREE_32NDS_A[action])
      localpatch = polygon(
          localpos, QPATCHSIZE / 2, color=localcolor, zorder=0
          )
      patches.append(qvaluepatch)
      patches.append(localpatch)
  return patches

def addpatches(axes, *patches):
  for patch in chain(*patches):
    if isinstance(patch, PatchCollection):
      axes.add_collection(patch)
    elif isinstance(patch, Patch):
      axes.add_patch(patch)
  return None

def notgoal(step):
  return not reachedgoal(step)

def takepathwhile(iterobj, predicate=None):
  if predicate is None:
    predicate = notgoal
  path = [START]
  
  while True:
    step = next(iterobj)
    path.append(step.sar.s)
    yield step, path
    if not predicate(step):
      path = [START]
  
# This is definitely not a scalable strategy for interfacing with a 
#   graphics module
# But here I am doing it
def drawevery(iterobj, threshhold=DEF_THRESHHOLD):
  stepandrecentpath = takepathwhile(iterobj)
  fig, axes = createplot()
  xs = list(X_RANGE)
  ys = list(Y_RANGE)
  walls = wallpatches()
  tiles = specialtilepatches()
  while True:
    step, path = next(stepandrecentpath)
    axes.clear()
    addpatches(axes, qvaluepatches(step))
    addpatches(axes, walls)
    addpatches(axes, tiles)
    addpatches(axes, currentstatepatch(step))
    addpatches(axes, currentactionarrowpatch(step))
    if len(path) > 2:
      pathpatches = pathpatchesfrom(path, threshhold, midpoint=0.75)
      addpatches(axes, pathpatches)
    statepatch = currentstatepatch(step)
    axes.set_xlim(X_LIMIT)
    axes.set_ylim(Y_LIMIT)
    xticks(xs)
    yticks(ys)
    for x in xs[:-1]:
      axes.axvline(
          x=x + 0.5, color='gainsboro', linestyle='dashed', zorder=0
          )
    for y in ys[:-1]:
      axes.axhline(
          y=y + 0.5, color='gainsboro', linestyle='dashed', zorder=0
          )
    draw()
    pause(PAUSE_SECONDS)
    yield step
    
if __name__ == '__main__':
  dq = tabdynaq(START, 10)
  i = drawevery(dq)
  i = waitforgoal(i, doallthosethings)
  i = dosteps(i, 100)
  step = next(i)