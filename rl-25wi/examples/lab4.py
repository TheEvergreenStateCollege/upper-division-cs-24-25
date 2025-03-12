#!/usr/bin/env python3

from collections.abc import Mapping
from functools import cache, partial
from itertools import accumulate, product, repeat
from random import choices
    
"""A module implementing lab 4 (gridworld using dynamic programming).

Taken from example 4.1 (Sutton & Barto p76).

Block quotes are narrative explanation (and/or docstrings - if you 
don't know docstrings, take a moment to read about docstrings).

Inline comments (with a '#') are asides and implementation notes. You 
can safely skip past them for most purposes, especially on your first 
read of the file. They're mostly preemptive answers to "Why'd you do 
that?"

I break from convention in one significant way in this file. Normally 
variables and functions should be in all lower case, and globals 
strictly upper case with underscores.

When I build an object that I intend to directly represent something 
from the book, I try to write the name how it appears in the book as 
much as possible. I find it hard to distinguish between these important 
objects and other globals I use to construct them along the way. So I 
don't always use caps for them. I use camel case to avoid making them 
longer with underscores, because they are important objects that I may 
refer to very often. I need them to be maximally readable without 
taking up a lot of space.

Conventions help reading! Don't break from them unless you have a 
compelling reason. If you do break them, be consistent in your own 
methods, and with the agreed upon practices of your work environment or 
project. Read the PEP 8 (Python Enhancement Proposal on code style), 
learn what a code linter is (like Black) and use it, and practice 
reviewing the writing of people contributing to the Python language. 
Not all languages have such an open community - it is something to be 
grateful for.

Counterintuitively, adhering to the standards can make it easier to 
understand other people's code, even when they don't follow regular 
style themselves. This is because the whole reason folks arrived at the 
standards is to address problems in understanding. Learning how the 
problems are prevented also helps one grasp their sources; once you can 
see the barriers to understanding, you can chart a path past them. 
Ultimately these conventions were distilled from the experience of 
countless experts who have come before us. They're worth the time.

Did you enjoy my reading guide/diatribe? Let's move on to "line one", 
LOL.
"""

__author__ = "Joe Granville"
__date__ = "20250204"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

"""This is a weird state space. It's like a grid, but it also wraps 
around on itself - the terminal state is linked to two opposite 
corners. Let's see if we can make something that has this unusual 
topology while still behaving like a grid.
"""

SCALE = 4
DIMENSION = 2
STATES_1D = frozenset(range(SCALE))
STATE_TUPLES = frozenset(product(*repeat(STATES_1D, DIMENSION)))
# product(*repeat(STATES_1D, N)) is equivalent to: 
# product(STATES_1D, ..., STATES_1D) N times. When * appears before a 
# sequence type like a list or tuple, it's called unpacking or "splat".

"""We can begin by making something that works entirely like a grid. 
After making a collection of grid coordinates for our states, we define 
a relationship that associates those states and movement actions with 
new states. Using grid coordinates lets us specify this in terms of 
vector math.
"""

@cache
def orthogonals(n):
  orthovectors = []
  for i in range(n):
    up = list(repeat(0, n))
    up[i] = 1
    down = list(repeat(0, n))
    down[i] = -1
    orthovectors.append(tuple(up))
    orthovectors.append(tuple(down))
  return orthovectors
  
ACTION_TUPLES = frozenset(orthogonals(DIMENSION))

@cache
def addtuples(a, b):
  return tuple(n + m for n, m in zip(a, b))
  
"""Rather than representing states outside the set of points we already 
defined, we'll just promise that every new state returned will be one 
of the existing points. In this particular case, the problem specifies 
that if the move selected from the current state would take us out of 
the grid, the result of the move is just the state unchanged.

States outside of the defined set of states formally do not exist in 
these types of problems, anyways. It is preferable if you can write 
your code such that it is simply not possible to represent invalid 
states. This is related to the concept of "invariance" - preserving 
the correct and true properties of data throughout the entire 
lifecycle of the calculation.
"""

@cache
def grid_transition(state, action):
  newstate = addtuples(state, action)
  if newstate in STATE_TUPLES:
    return newstate
  else:
    return state

"""The problem asks us to name our states with integer labels as 
illustrated in the figure. States at (0, 0) and (3, 3) aren't given 
names, and more curiously we are asked to consider them the same state. 
The grid representation we have properly represents movement relative 
to these states and their neighbors, but it would be helpful if we 
could forget about (0, 0) and (3, 3) once we get there and consider 
them identical at a more abstract level.

A related concept in mathematics is equivalency classes. In short, an 
equivalency class is a function that sorts objects into distinct 
classes. By distinct class, I mean that each object gets assigned to 
exactly one class. Geometric shapes are not equivalency classes, 
because for instance a given shape can satisfy many definitions - a 
square is also a rectangle and a quadrilateral. Even and odd integers 
are equivalency classes. Assignment - the equals sign or "identity" in 
mathematics - is the trivial equivalency class. The "identity" class 
basically says, for every object, that object belongs to the class that 
contains just that object. Cute right?
"""

CURLY_S = frozenset(str(n) for n in range(1, len(STATE_TUPLES) - 1))
TERMINAL_STATE = 'T'
TERMINAL_S = frozenset(TERMINAL_STATE)
CURLY_S_PLUS = CURLY_S | TERMINAL_S

ENUMERATED_STATES = enumerate(list(sorted(STATE_TUPLES)))

"""We can create an equivalency class that gives a label for each grid 
point. To be an equivalency class, we must assign exactly one label to 
each item in the "domain" that the class is defined over - in this 
case, our state tuples. First we label each point in order, left to 
right, top to bottom. Python hashes tuples in a strange order for fast 
searches but it sorts them a lot like numbers or strings - from left to 
right. 'sorted(STATE_TUPLES)' sorts by the first element first, then 
the second and so on. The ordering starts at (0, 0) and counts up 
through all the values in row 0, then wraps around again to row 1 at 
(1, 0) and so on.

Then we overwrite the labels for (0, 0) and (3, 3) so that they point 
to the same value. Multiple items in the domain are allowed to occupy 
the same class. This is one place where value objects really excel, 
because we can think of them as representing the same thing wherever we 
find them, rather than having to inspect their contents like containers 
or other entity objects. (I'm spoiling exercise 4.2 here, but it wasn't 
assigned anyways.)
"""

STATE_LABEL = {s: str(i) for i, s in ENUMERATED_STATES}
# If I were being extra tidy, I'd try to find a way to do this without 
# 'enumerate()' or explicit 'i' values. If we were working with too 
# many labels to check by hand, it would be good to have an algorithm 
# that assures that the labels used in 'STATE_LABEL' are exactly the 
# same as those that we constructed for CURLY_S - not by safety 
# checking the values, but by always actually using the same symbol 
# (reference or name) in code throughout construction of both data 
# structures. Strings are value types, so we can let it slide for now, 
# but imagine how confusing it might be if we assigned labels 
# inconsistently and label '1' meant one thing in a certain part of the 
# code, but was related to a different grid point elsewhere. It's good 
# to look for ways to prevent such mixups structurally.

UPPER_LEFT = tuple(repeat(0, DIMENSION)) # All 0s
LOWER_RIGHT = tuple(repeat(SCALE - 1, DIMENSION)) # All 3s or something

STATE_LABEL[UPPER_LEFT] = TERMINAL_STATE
STATE_LABEL[LOWER_RIGHT] = TERMINAL_STATE

"""The number of states is finite, so we can exhaustively search every 
possible state-action pair and represent the relationship as a 
dictionary from function parameters to return values. This is sometimes 
called a mapping or image - it represents the results of a mathematical 
function as a collection of values. (Fun fact: if you see the @cache 
function decorator elsewhere in my code, it does the same thing - wraps 
the decorated function with a dictionary to store previous results. 
Here it's preferable if we can directly manipulate the dictionary, 
though, whereas @cache is invisible. It's meant to be indistinguishable 
from the original function it wraps.)
"""

# First a collection of all possible state-action pairs, as tuples
SA_PAIRS = frozenset(product(STATE_TUPLES, ACTION_TUPLES))
# Now names are getting complicated - next is the grid transition 
# function with states labeled:
T_LABELED_S = {}
for s, a in SA_PAIRS:
  T_LABELED_S[STATE_LABEL[s], a] = STATE_LABEL[grid_transition(s, a)]

"""We compose the state transition relationship with the equivalency 
class of state labels. Taking the image of these composed functions 
gives us a transition table that goes from labeled states and actions 
to labeled states.

In the general case this might lead to key-value pairs that overlap 
when two states are merged into one label, but because we are taking 
opposite corners, the resulting merged state will only have one 
neighbor on each side. If you were to merge two states that have 
unique neighbors in the same relative direction, you'd have to have 
some method of picking one neighbor or another, or a representation 
that didn't require you to choose a single neighbor per direction/
action.

But the upper left corner has no neighbors above or to the left, and 
the lower right has no neighbors below or to the right, so they're 
ideal candidates for collapsing into an equivalent state. We also stop 
moving once reaching the terminal state, so it would be OK to have lots 
of states dump into it, so long as we're not expected to be able to 
move back out along a symmetrical path. To be especially correct, we'll 
knock out all the state-action pairs moving out of the terminal state 
because those transitions should not exist in our MDP transition 
function according to the problem definition.
"""

for (state, action), newstate in list(T_LABELED_S.items()):
  if state in TERMINAL_S:
    del T_LABELED_S[state, action]

"""The result is a transition function specified entirely in terms of 
the requested state labels, no coordinates required. We can go a step 
further and similarly replace the tuples representing actions with 
strings or other more legible representations like sentinel objects.
"""

DIRECTIONS = [
    ('right', 'left'), 
    ('up', 'down'), 
    ('in', 'out'), 
    ('before', 'after')
]

def labelunitorthogonals(n, labels=DIRECTIONS):
  digits = len(str(n))
  orthovectors = orthogonals(n)
  # Sequence[1::2] means start at index 1 and take every 2nd item after
  oppositepairs = list(zip(orthovectors[::2], orthovectors[1::2]))
  ortholabelmap = {}
  # Normally we'd prefer zip to explicitly indexing into the lists, but 
  # we have an extra use for i
  for i in range(n):
    up, down = oppositepairs[i]
    if i < len(labels):
      ulabel, dlabel = labels[i]
    else:
      ulabel = 'd' + f'{i:0{digits}}' + 'plus'
      dlabel = 'd' + f'{i:0{digits}}' + 'minus'
    ortholabelmap[up] = ulabel
    ortholabelmap[down] = dlabel
  return ortholabelmap

ACTION_LABEL = labelunitorthogonals(DIMENSION)
CURLY_A = frozenset(ACTION_LABEL.values())

"""This does introduce another idiosyncratic transformation that's 
particular to this problem, so it requires some extra detail. But now 
we're equipped to completely remove the remaining tuples representing 
our available actions.
"""

T_LABELED_SA = {}
for (state, action), newstate in T_LABELED_S.items():
  T_LABELED_SA[state, ACTION_LABEL[action]] = newstate
  
"""Dictionaries have an important difference from the mathematical 
notion of mappings and functions; dictionaries are mutable. It's useful 
here to use dictionaries while we build all the values needed for the 
mapping, but it might be good to not allow changes beyond this point 
now that we are done calculating the mapping, lest we forget or make a 
mistake like typing "=" instead of "==".

If you're disciplined you can get away with using mutable types and 
just promising not to change them. But mutable types are also not 
hashable; plus we get some freebies in return for our trouble when we 
identify opportunities to instead use an immutable representation. (Of 
course, Python happily permits you to provide hash values for mutable 
classes you write yourself, but they won't behave correctly unless you 
treat them as immutable.)
"""

# Generally I avoid implementing error checking, but when writing a 
# mapping I need to allow for the real possibility that the user may 
# ask for a key that is not stored, as that's just part of life for a 
# mapping type. When you know a regular use case exists that will 
# cause the error, then regular checking becomes prudent. Defining and 
# throwing our own custom exceptions helps to distinguish between bugs 
# that originate in our code and exceptions that are thrown by 
# libraries we've included.
class CustomException(Exception):
  pass

class CustomKeyError(CustomException, KeyError):
  pass
  
class FrozenMap(Mapping):
  def __init__(self, arg, **kwargs):
    if isinstance(arg, Mapping):
      pairs = arg
    else:
      pairs = kwargs
    
    self.pairs = frozenset(pairs.items())
    
    return None
    # The return value of __init__() must always be None. It's OK to 
    # omit this but it helps to visually identify the end of the method 
    # in a crowded class definition.
  
  def keys(self):
    return dict(list(self.pairs)).keys()
    
  @cache
  def domain(self):
    return frozenset(self.keys())
    
  def values(self):
    return dict(list(self.pairs)).values()
  
  @cache
  def codomain(self):
    return frozenset(self.values())
  
  def __eq__(self, other):
    if not isinstance(other, FrozenMap):
      return False
    return self.pairs == other.pairs
  
  def __hash__(self):
    return hash(self.pairs)
    
  @cache
  def __getitem__(self, key):
    try:
      value = next(v for k, v in self.pairs if k == key)
    except StopIteration as e:
      # Of course, I'll never forget and ask for a key I haven't 
      # stored, but if I did, I'd get an informative error
      raise CustomKeyError from e
    return value
  
  def __iter__(self):
    return iter(k for k, _ in self.pairs)
  
  @cache
  def __len__(self):
    return len(self.pairs)
    
  @cache
  def __repr__(self):
    return f'FrozenMap({dict(self.pairs)})'
    
  @staticmethod
  def freezeimage(domain, valuemap):
    if isinstance(valuemap, Mapping):
      get_ = valuemap.get
    else:
      get_ = valuemap
    
    pairs = {key: get_(key) for key in domain}
    
    return FrozenMap(pairs)

  @staticmethod
  def uniquekeys(pairs):
    ks = frozenset(sorted(k for k, _ in pairs))
    uniquekeypairs = {}
    for key in ks:
      for k, v in pairs:
        if k == key:
          uniquekeypairs[k] = v
          break
    return uniquekeypairs
       
BIG_P = FrozenMap(T_LABELED_SA)

"""A user might change a dictionary by accident. FrozenMap values can 
be changed, too - but it's hard to do without being deliberate. They 
can't be assigned with a normal '='; you have to know where the 
attributes are saved within the class definition and tamper with them 
directly. That's a reasonable amount of guardrails. In the Python 
community we say, "We're all adults here."

We now have a relationship that has adjacencies like a grid, but with a 
special terminal state that folds around from opposite corners. The 
adjacencies are labeled, according to the associated action. A mapping 
or dictionary which goes from a set of (node, edge) -> node is also a 
graph. (Like, the kind of mathematical graphs that include tree 
structures.)

More specifically, it is a labeled directional graph. Distilling our 
representation to these terms allows a great deal of flexibility; we 
can now "punch out" arbitrary parts of the grid, fold it around on 
itself, "pinch" or "merge" states together, and it's imaginable that we 
could even link multiple grids in strange topologies with a little more 
deliberation.

The definition of state transitions under MDPs (as well as finite state 
machines, their simpler deterministic cousins) are equivalent to 
labeled digraphs structurally. This kind of equivalency between 
mathematical or logical structures is also referred to as being 
homomorphic, or having the same algebraic features. Algebras are great 
places to mine for programming insights because they're all about 
generalizable rules and operations.
"""

# SA_PAIRS has some pairs we removed from BIG_P when deleting arcs from 
# the merged terminal state, so we'll just use the pairs that made it 
# all the way into BIG_P when defining our reward function.
BIG_R = FrozenMap({(s, a): -1.0 for s, a in BIG_P.domain()})

"""Gratefully, after all that work to construct a warpy gridworld, the 
reward function is dead simple. What kind of evaluation are we doing on 
this? I wasn't paying attention. Going to look at the lab assignment.
"""

pass
# The Python community sometimes says that Python is "pseudocode that 
# runs". Anywhere you need a statement in Python, you can write '...' 
# or 'pass' as a placeholder if you haven't yet decided what goes 
# there. Then you can just go on building the rest of the structure of 
# your code. They both mean "no instructions", essentially. I like to 
# use '...' for things I need to come back to, and 'pass' when I'm 
# explicitly skipping something and don't intend to change it.

"""Right, now I remember. There's another trick to this - we're looking 
for a non-deterministic policy. We could just define a policy method 
that makes a random choice when there is more than one greedy action 
(IE they are tied for the same maximal value). That's not real enough 
for me though. The real formula on a blackboard would be a mathematical 
expression that represented the probability.
 
When you make a real-life concept real in code, that's reification. 
It's a little overkill for a one-off task like this, but it's a good 
mental exercise and - like many design techniques that have been honed 
by experts - it usually results in code that is at least a little more 
correct and flexible.

What we want here is something that works like a value object - we can 
return it from a function or use it to represent the values in a 
dictionary or other mapping. We can compare it to other objects and say 
whether or not they are equal. It should store all the information we 
need to make the random choice that the distribution represents, but 
support our making the choice whenever we decide - not just when the 
state-action pair is looked up in the agent's policy.
"""

class FiniteDistribution(Mapping):
  def __init__(self, domain, mapping):
    self.domain = frozenset(domain)
    self.mapping = FrozenMap(mapping)
    return None
  
  def keys(self):
    return dict.fromkeys(domain, []).keys()
    
  @cache
  def domain(self):
    return frozenset(self.keys())
    
  def values(self):
    return self.normweights.values()
  
  @cache
  def codomain(self):
    return frozenset(self.values())
    
  def __call__(self):
    return self.choose()
  
  def __eq__(self, other):
    if not isinstance(other, FiniteDistribution):
      return False
    domaineq = self.domain == other.domain
    mappingeq = self.mapping == other.mapping
    return domaineq and mappingeq
  
  def __hash__(self):
    return hash((self.domain, self.mapping))
    
  @cache
  def __getitem__(self, key):
    if key not in self.domain:
      raise CustomKeyError
    else:
      return self.p(key)
  
  def __iter__(self):
    return iter(var for var in self.domain)
  
  @cache
  def __len__(self):
    return len(self.domain)
    
  @cache
  def __repr__(self):
    domain = self.domain
    mapping = self.mapping
    attributes = f'domain={domain}, mapping={mapping}'
    return f'FiniteDistribution({attributes})'
  
  def choose(self):
    return choices(list(self.domain), cum_weights=self.weights)
    
  @property
  @cache
  def normweights(self):
    domain = list(self.domain)
    map_ = self.mapping
    maxweight = self.weights[-1]
    normweights = [map_[var] / maxweight for var in domain]
    return FrozenMap(dict(zip(domain, normweights)))
    
  @cache
  def p(self, var):
    return self.normweights[var]
  
  @property
  @cache
  def weights(self):
    domain = list(self.domain)
    map_ = self.mapping
    weights = [map_[var] if var in map_ else 0.0 for var in domain]
    return tuple(accumulate(weights))
  
  @staticmethod
  def linear(domain):
    mapping = FrozenMap({var: 1.0 for var in domain})
    return FiniteDistribution(domain, mapping)
    
  @staticmethod
  def normalized(domain, mapping):
    distribution = FiniteDistribution(domain, mapping)
    return FiniteDistribution(domain, distribution.normweights())
    
  @staticmethod
  def mixture(distributions):
    domain = set()
    mix = {}
    for dist, distw in distributions:
      domain = domain | dist.domain
      for var, varw in dist:
        mix[var] = mix.get(var, 0.0) + distw * varw
    return FiniteDistribution(domain, mix)

"""Here we've made FiniteDistributions callable like a function, so 
that distribution() performs a random trial. We've also made it 
indexable like a dictionary or other mapping, so that distribution[var] 
returns the weighted probability associated with the random variable 
var.

FrozenMap does a fair amount of the heavy lifting here, and I could 
have chosen to subclass FrozenMap, but I migrated this from a design 
that used a different base class. Rather than subclassing or mixing in 
the FrozenMap class, I just have a FrozenMap attribute - this gets me 
almost all the same functionality, and I don't have to worry about 
clashing definitions from parent classes and mixins. This is called 
"composition over inheritance" or the "composite reuse principle".

Basically a distribution is a mapping from a collection of objects to 
probability values. I chose to explicitly define a domain attribute 
because sometimes we may have many items for which the weight or 
probability is zero and I thought it might be easier if we could omit 
zero values when constructing the associated mapping.
"""

AVAILABLE_ACTIONS = {}
for s, a in BIG_P.keys():
  AVAILABLE_ACTIONS[s] = AVAILABLE_ACTIONS.get(s, []) + [a]
for s, as_ in AVAILABLE_ACTIONS.items():
  AVAILABLE_ACTIONS[s] = frozenset(as_)
CURLY_A_SUB = FrozenMap(AVAILABLE_ACTIONS)

# Long name alert: equiprobable random policy
EQRANDPI = {s: FiniteDistribution.linear(CURLY_A_SUB[s]) 
            for s in CURLY_S}
# FiniteDistribution.linear() does all the menial work around counting 
# available actions and giving a probability for each one. We could 
# instead create a hexagonal grid, or some irregular shape like a 
# traffic routing graph, and this bit of code wouldn't complain or even 
# notice. The key is that CURLY_A_SUB lets me completely forget about 
# why states are related to actions and boils the relationship down to 
# just a yes/no answer about what is available.

"""Non-programming intermission!

The lab instructions fail to mention a key detail. Did you spot it 
before my last derivation?

If you merely look at the definition in example 4.1, it only gives 
enough information to construct the environment. Exercise 4.1 hints a 
bit more at what is missing: a policy. Iterative Policy Evaluation is 
only defined in terms of a specific policy pi. A policy is a required 
input to the algorithm - without one there's no calculation to do. The 
results depicted in figure 4.1 are based on the random policy.

Learning how to gather and assess the requirements of your task is an 
extremely critical skill as a software engineer. It is arguably more 
important than raw talent or knowledge of specific tools.
"""

def qvalues(states, other={}):
  q = {}
  for state in states:
    q[state] = other.get(state, 0.0)
  return q
emptyqs = partial(qvalues, CURLY_S_PLUS)

def greedypi(q):
  pi = {}
  for state in q:
    if state not in CURLY_S:
      continue
    actions = CURLY_A_SUB[state]
    neighborvalfun = lambda a: q[BIG_P[state, a]]
    maxaction = max(actions, key=neighborvalfun)
    maxvalue = neighborvalfun(maxaction)
    maxactions = [a for a in actions if neighborvalfun(a) == maxvalue]
    pi[state] = FiniteDistribution.linear(maxactions)
  return FrozenMap(pi)
  
# Did you notice FiniteDistribution.mixture()? I actually just wrote 
# that right now and added it to my copy of the class in another file 
# too. A mixture distribution is a conventional mathematical derivation 
# that lets us combine multiple separate distributions based on a 
# "distribution of distributions." So we can do this:
def epsilon(pi, e):
  epsdist = FiniteDistribution({EQRANDPI: e, pi: 1.0 - e})
  return FiniteDistribution.mixture(epsdist)
  
"""Now we have a means to construct a dictionary representing Q values. 
The method can duplicate values from an existing dictionary or generate 
all zero values based on a given collection of states. I chose to use a 
dictionary because there are meaningful differences in implementing 
policy improvement between copying from one dictionary to another as 
opposed to update-in-place.

We also have a method which calculates the greedy actions according to 
a Q value mapping, and returns a policy of probabilities expressed by 
FiniteDistribution objects. With some extra cross-multiplication we can 
use this representation to automatically generate an epsilon-greedy 
policy in the same form.

We're close to done! I'm going to diverge from the exact definition in 
the book a little and create a convenience function for calculating the 
error term. (Bonus points: doing so results in a slight speedup. Can 
you tell why?) The algorithm on p75 is slightly wrong, anyways - notice 
that the final line is not indented at all, suggesting we should return 
to the outer loop and set delta to 0 again. So I fixed it based on what 
I gathered from descriptions of the meaning and properties of iterative 
policy evaluation found throughout the chapter.
"""

# This would be useful for other algorithms that converge towards a 
# Q value mapping, so it's worth defining independently.
def maximumqerror(q, qprime):
  return max(abs(q[s] - qprime[s]) for s in q.keys())
  
def policyevaluation(q, pi, gamma):
  qprime = qvalues(q.keys())
  # The sum simplifies quite a bit because the environment is 
  # deterministic; there is only one possible new state for each 
  # state-action pair, and only one reward, so we don't need to iterate 
  # over possible values for s' or r or their respective probabilities
  rs = lambda s, a: BIG_R[s, a] + gamma * q[BIG_P[s, a]]
  for s in CURLY_S:
    # rs has a reference to our q dictionary so it can see value 
    # updates even though q comes from an outside variable scope
    qprime[s] = sum(pi[s].p(a) * rs(s, a) for a in pi[s])
  return qprime
# For those curious, an inline version of the sum would read:
# qprime[s] = sum(pi[s].p(a) * (BIG_R[s, a] + gamma * q[BIG_P[s, a]]) 
#                 for a in pi[s]
#                )
# Which version do you find easier to understand? No wrong answer.

"""You might notice that the comments get longer and the code itself 
gets shorter (in general, but not everywhere) as I go. That's a result 
of reification. Each following expression tends to mean more, because 
it builds on the behavior of what came before. I'm constructing parts 
that increasingly describe exactly the properties I'm working with, so 
my code over time becomes more about the problem domain and less about 
Python itself. It's just like any other language - bigger, more 
specific or more complicated words let you express more in a single 
thought.

My mindset when I start to build is actually to forget or dismiss as 
much of the specifics about Python and the rest of my programming 
environment as I can. I want to be strongly connected to the concept, 
and weakly connected to the tools I use to get there. Tools are 
ephemeral; the concept is what must always remain true. Well-designed 
software has obvious and sensible boundaries or "seams" where it can be 
cut free of its existing environment and migrated to another without 
changing its internal meaning and correctness.

My goal is not to talk Python. My goal is to describe all the atoms I 
need to talk about the problem. My goal is to _not talk Python_. This 
can be referred to as "loose coupling".

If something is useful, I bind it to a meaning in my reified model of 
the problem. If it's not useful, I isolate it from the "safe zone" of 
correct behavior I am carving out. Preferably, I can just ignore it. At 
the end of a work session I am looking for my code to say relatively 
less about my tools, and distinctly more about my problem domain. Of 
course in practice, there's only so much you can realistically trim.

If you don't find yourself getting more and more done as you progress 
on a programming task it's a sign that there is room for improvement in 
your organization and framing of the problem. Good design tends to lead 
to "aha" moments and productivity that curves up (gently) over time 
instead of plateauing. Good solutions start to pull you towards true 
understanding as you near the right answer, like a magnet snapping into 
place.

That said, some problems are still a slog despite the best of habits. 
Sometimes the magnet just pulls straight toward the fridge door, even 
if you meant to put it in a slightly different position. And as you can 
see here, adhering to a structured design technique does tend to come 
with some upfront overhead, so it is often slower to start.
"""

def simple_ipe(q, pi, delta, gamma):
  while True:
    qprime = policyevaluation(q, pi, gamma)
    if maximumqerror(q, qprime) < delta:
      break
    q = qvalues(qprime.keys(), qprime)
  return qprime

def iterativepolicyevaluation(q, pi, delta, gamma, timeout=1E9):
  if delta > 0.0:
    terminalcondition = lambda q_, qp_: maximumqerror(q_, qp_) < delta
  else:
    terminalcondition = lambda q_, qp_: greedypi(q_) == greedypi(qp_)
  for _ in range(int(timeout)):
    qprime = policyevaluation(q, pi, gamma)
    if terminalcondition(q, qprime):
      break
    q = qvalues(qprime.keys(), qprime)
  return qprime
  
"""If delta is 0.0 or less, the given algorithm would never terminate. 
So I added a little extra here. If we get a nonsensical value, we 
instead iterate up to a certain step limit, or until the greedy policy 
converges and stops changing. Rather than write two separate loops, 
it's possible to store the expression for terminating the loop as a 
value in a variable.

In Python, variables can contain references to functions. Then you can 
apply inputs to the variable and it will be called like any other 
function. When a language can manipulate functions and other code in 
the same terms as variables and literal values, we say that functions 
are "first-class objects" or that the language has "first-class 
functions". By storing a function in terminalcondition and then calling 
terminalcondition() to determine when to break the loop, we can write a 
single piece of code that has the same control flow but represents many 
different possible operations or functionalities. This is frequently 
used in Python. 

For instance, the built-in sorted() function returns the elements in a 
List or Sequence, sorted by their numeric representation (specifically, 
the magic methods defining the "less than/greater than" relationships 
on a type). But if you include an optional key= value in the 
parameters, sorted() will call key() for every item being compared, and 
will use the results of key() to sort the items instead of the numeric 
value of each one. max() and min() have the same optional parameter. 
Similar facilities exist for searches/traversals and many other common 
operations.
"""

# How to drive this code:
# Try the following in interactive Python

# 0: Open this file in the interactive interpreter
# From the same directory as this file, type just 'python' to start the 
# interpreter. Then, to load this file, type 'import lab4'
# 
# This will load the file as a module - you'll need to access its 
# contents using 'lab4.' such as 'lab4.CURLY_S'
# 
# If you type 'dir(lab4)' you'll get a list of all the named objects 
# contained in this file, including variables, function definitions and 
# class declarations.
# 
# In interactive Python it can be easier to write 'from lab4 import *'
# Using 'from' imports symbols into the local namespace, so you can 
# access them without the 'lab4.' Using the star means you import 
# everything contained in the module.
# 
# Never use 'from <blah> import *' in your files. It is unclear to 
# readers and can create hard-to-track bugs when modules have objects 
# with conflicting names. If you know you need an object, you can name 
# it. If you need everything in the module, use the module name or use 
# something like 'import <inconvenientlylongname> as <nickname>'
# 
# It would be difficult to permanently break anything in this 
# environment, but it is possible to overwrite values loaded from the 
# file. If things stop working, type 'exit()' to leave Python and then 
# start it again.
# 
# Make sure you learn to use dir() in the interpreter! Make sure you 
# learn to use the interpreter! Many questions I am asked in class can 
# be answered with the interpreter and a handful of built-in functions 
# like dir(), type() and isinstance().

# 1: Inspect the representative objects
# Sets:
CURLY_S # All non-terminal states
CURLY_A # All actions
TERMINAL_S # All terminal states
CURLY_S_PLUS # All states
# Functions represented as piecewise dictionaries:
BIG_P # The state transition function
BIG_R # The reward function
CURLY_A_SUB # The actions available at each state
EQRANDPI # The equiprobable random policy
# Sets can be tested for membership of an element:
'down' in CURLY_A # should return True
'1' in TERMINAL_S # should return False
# Function dictionaries can be tested for defined values/keys:
'1' in CURLY_A_SUB
stateaction = ('1', 'down')
stateaction in BIG_P
# Function dictionaries can also be subscripted to get their elements:
CURLY_A_SUB['1'] # actions available from state 1
BIG_P['1', 'down'] # state that results from moving down from state 1
BIG_R['1', 'down'] # reward that results from moving down from state 1
# When more than one value is passed in a subscript, it is interpreted  
# as though those values were in a tuple. The following are equivalent:
BIG_P['1', 'down']
BIG_P[('1', 'down')]
BIG_P[stateaction]

# 2: Inspect the FiniteDistribution class
dir(FiniteDistribution)
randomten = FiniteDistribution.linear(range(10))
randomten
dir(randomten)
randomten.domain # The set of variables (objects) that can be chosen
randomten.mapping # The relative weight of choosing each variable
randomten() # Perform a random trial based on the weights in mapping
[randomten() for _ in range(9)] # List of nine random draws
[randomten() for _ in range(9)] # List of nine different draws
randomten[1] # Weight for choosing the integer 1
randomten.p(1) # Normalized probability of choosing the integer 1
# p() is the weight of the item divided by the total of all weights

# 3: Create an empty Q value dictionary
q = emptyqs()
q

# 4: Create a function dictionary for the greedy policy given Q values
greedypiq = greedypi(q)
greedypiq
# Because the Q values are all zero, the policy isn't very meaningful
greedypiq == EQRANDPI
# Because the keys and values of each policy dictionary are all value 
# objects, Python can automatically check equality by just checking 
# each respective object the dictionaries contain.

# 5: Calculate Q values using iterative policy evaluation
q2 = emptyqs
q = iterativepolicyevaluation(q, EQRANDPI, 0.00001, 1.0)
q2 = iterativepolicyevaluation(q2, EQRANDPI, 0.0, 1.0)
q
q2
q == q2 # Should return False

# 6: Generate policies based on the Q values
pi = greedypi(q)
pi2 = greedypi(q2)
pi == pi2 # Should return True

"""As mentioned earlier, you won't learn design skills from typical 
computer science textbooks or programming tutorials. You have to 
deliberately go out and seek sources that are specifically about 
software engineering, architecture, design, working in teams and the 
business of managing programmers.

Many people in the field choose to turn away from this, because those 
that are technically inclined tend to prefer working on technical 
things. They are typically most comfortable within a zone of expertise 
where their understanding and techniques work reliably and need not be 
challenged.

Ultimately design is actually more of a people skill, hinging on 
communication with your team/clients and the ability to observe the 
perspective/needs of others - as well as self-discipline, introspection 
and a drive for continual improvement. Taking on this mantle can move 
you into a slightly different domain of work than most programmers.

Design is an intimidating subject to break into, but it's worth its 
figurative weight in gold (because learning is intangible). It will let 
you fly where you once struggled to walk. Learning to program is like 
learning to vocalize; what comes out doesn't necessarily have meaning. 
It's hard to adopt a language in the absence of other people's 
knowledge. Design is where you really start learning to communicate 
with other programmers - it's speaking in cogent sentences, about ideas 
that are coherent and consistent with the knowledge of others.

The real power of engineering and mathematics is being able to leverage 
the insights of our predecessors and have them manifest as real 
tangible things, not just a tradition of craft or form. Emulation of 
technique alone isn't sufficient. The magic comes from truly 
transmitting understanding.

I hope this was of some help. Thank you for your time and 
consideration.

~Joe

Key references:
https://peps.python.org/pep-0008/
https://peps.python.org/pep-0257/
https://docs.python.org/3/
https://docs.python.org/3/library/functions.html
https://docs.python.org/3/tutorial/interpreter.html#interactive-mode
https://github.com/psf/black
Martin, Robert Cecil. 2003. Agile Software Development: Principles, 
  Patterns, and Practices. Prentice Hall.
Evans, Eric. 2003. Domain-Driven Design: Tacking Complexity In the 
  Heart of Software. Addison-Wesley Longman.
Slatkin, Brett. 2019. Effective Python: 90 Specific Ways to Write 
  Better Python. Addison-Wesley Professional.
"""