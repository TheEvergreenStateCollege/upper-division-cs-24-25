#!/usr/bin/env python3

from abc import ABC, abstractmethod
from collections.abc import Mapping
from functools import cache
from itertools import product, repeat
from random import choice, random, sample
from typing import get_args, Union
    
"""A module implementing labs 5 and 6 (blackjack).

Taken from example 5.1 (Sutton & Barto p93).

I think calling finishing the hand "sticking" sounds pretty weird. I'm 
almost certain I've always heard it referred to as "stay".
"""

__author__ = "Joe Granville"
__date__ = "20250204"
__license__ = "GPL"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"

"""Today I'll introduce (subject?) you to some type mechanisms. Python 
is strongly typed - meaning objects have distinct types. But Python is 
also dynamically typed - meaning that a given variable can hold any 
type of object, depending just on what is assigned to it.

You may have come from statically typed languages like the C family. 
When a language is statically typed, variable names have set types that 
do not change, even if you can change the value associated with that 
variable. The language can then make some decisions at compile time to 
determine whether or not certain values make sense - trying to store a 
float into an int in C++ results in a type mismatch. The compiler then 
quietly adds in a typecast to round your float to an int, assuming 
that that's what you would have meant. And if it can't decide what you 
meant, like if you assign a class object to a raw byte variable, it 
will fail to compile and tell you something looks wrong.

For better and worse, Python is much more permissive. Python uses "duck 
typing", as in "if it looks like a duck and quacks like a duck, it is a 
duck". Under the hood, Python doesn't care a lot about types - what it 
cares about is having methods it can use on those types. For instance, 
you can use <, >, <=, >= and == on all sorts of types and it doesn't 
matter much if they don't match - Python will make a comparison so long 
as it can find the special methods __gt__(), __lt__(), __eq__(), etc. 
which define numeric comparisons for such objects. These are also 
called magic or dunder methods - "dunder" being short for "double 
underscore". Python places the responsibility in your hands for making 
sure a given value suits the needs of the operations you perform on it.

You're not all alone in this, though. Python provides lots of optional 
tools to remove the guesswork. Code linters like Black replace some of 
the "sensibility check" functions of static type checkers. Python also 
has a feature called "type hints". These are essentially metadata 
values you can place in your code voluntarily, that then work with 
Python debugging and code profiling tools to provide type checking and 
additional conveniences through unit testing suites and other 
customizable helpers.

If you're interested in type hints, check out PEP 484, linked at the 
end of this file. Most PEPs are also easy to find on a search engine;  
they get lots of traffic.

We won't get that far today. I'm going to begin with subclassing value 
types. The resulting type has all the properties of the parent type or 
class, but is strictly a subtype of the parent type.

In Python, int() creates an int, str() creates a str, and so on. By 
subclassing an int, you can create a type Foo which has all the 
properties of ints, but can be distinguished from them by type.

This may seem trivial, but it can really help when you have elementary 
values that are the same base type but mean necessarily distinct things 
in your data model. A foo can be used anywhere an int can, but we can 
easily distinguish foos from other ints. type(int(1)) != type(Foo(1)), 
and that's something you can check at run time. (Or even before then 
with hints.)
"""

class Lab5Exception(Exception):
  pass
  
class Lab5NotImplementedError(Lab5Exception, NotImplementedError):
  pass

class CardT(int):

  _CARD_STRINGS = {2: 'TWO', 3: 'THREE', 4: 'FOUR', 5: 'FIVE', 
                   6: 'SIX', 7: 'SEVEN', 8: 'EIGHT', 9: 'NINE', 
                   10: 'TEN', 11: 'ACE'
                  }
                 
  def __repr__(self): # the "serializable/reproducible" representation
    return f'CardT({super().__repr__()})'
    
  def __str__(self): # the "pretty print" representation
    return type(self)._CARD_STRINGS[self]
    
DECK_INTS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11)
CARD_DECK = tuple(CardT(n) for n in DECK_INTS)
CARDS = frozenset(CARD_DECK)
ACE = CardT(11)

class ScoreT(int):

  def __repr__(self):
    return f'ScoreT({str(int(self))})'
    
  def __str__(self):
    return super().__repr__()
    
TWENTYONE = ScoreT(21)
NONTRIVIAL_THRESHOLD = ScoreT(12)
NONTRIVIAL_INTS = frozenset(range(NONTRIVIAL_THRESHOLD, TWENTYONE))
NONTRIVIAL_SCORES = frozenset(ScoreT(n) for n in NONTRIVIAL_INTS)

"""TWENTYONE is the winning score. I felt it would be confusing to name 
this value BLACKJACK because blackjack refers not just to a score or 
type of hand, but specifically the circumstances where the player 
receives an ace and a ten as their hand on the first turn, without 
acting. That's more specific than just a state, because it specifies 
the point in the episode where that state must occur, too.

The definition of MDPs we're working with don't do a great job of 
telling how to represent trials where an agent can complete an episode 
before even acting, so I'm going to have to hand-wave the rules around 
winning by blackjack. You may notice later on that I include blackjack 
hands in the value estimates. This is because my implementation will 
try to tabulate rewards collected on automatic wins, even if the policy 
is trivial at those state-action pairs - since the win happens before 
the agent's action is ever evaluated by the environmental model.
"""

class HasAceT(int):
  """We want a value to indicate the availability of a usable 
  (reducable) ace. It should be truthy, but bool is not available to 
  use for a base type. bool is an instance of int though, so int must 
  be truthy too - we'll use that.
  
  This is a docstring! You can see it in interactive Python as 
  'lab5.HasAceT.__doc__' - try it!
  """
  def __repr__(self):
    """It still prints like an int so we'll sneak the real True and 
    False in for string-representation purposes.
    """
    return f'HasAceT({str(bool(self))})'
    
  def __str__(self):
    return 'HasAce' if self else 'NoAce'
  
  @property
  def char(self):
    """An alternative to HasAceT.__str__() for single-character output.
    """
    return 'A' if self else '~'
    
NOACEVAL = HasAceT(False)
HASACEVAL = HasAceT(True)
HASACEVAL_BOOLS = frozenset([NOACEVAL, HASACEVAL])

class HandT(tuple):

  def __new__(cls, score, hasace):
    return super().__new__(cls, (score, hasace))
    
  def __repr__(self):
    return f'HandT({self[0].__repr__()}, {self[1].__repr__()})'
    
  def __str__(self):
    return f'{str(self[0])}{self[1].char}'
    
HANDS_PRODUCT = frozenset(product(NONTRIVIAL_SCORES, HASACEVAL_BOOLS))
NONTRIVIAL_HANDS = frozenset(HandT(*hand) for hand in HANDS_PRODUCT)
EMPTY_HAND = HandT(ScoreT(0), NOACEVAL)
TWENTYONE_HAND = HandT(TWENTYONE, NOACEVAL)
TWENTYONE_ACE_HAND = HandT(TWENTYONE, HASACEVAL)
WINNING_HANDS = frozenset({TWENTYONE_HAND, TWENTYONE_ACE_HAND})
PLAYABLE_HANDS = NONTRIVIAL_HANDS | WINNING_HANDS

class StateT(ABC):
  """Abstract base class for states.
  """
  
  @abstractmethod
  def ppstate(self):
    raise Lab5NotImplementedError("Missing definition for 'ppstate'")

"""Terminal states in episodic processes are often very different from 
working, non-terminal states. Terminals generally indicate only a final 
result or even just a status code indicating success or error; working 
states typically need to store more information for making calculations 
related to the problem.

Abstract base classes contain no code - only declarations of code that 
an inheriting class should provide. They are similar to interfaces in 
Java or virtual functions in C++ and related languages. An abstract 
base class is a way of expressing expectations of what the inheriting 
class should be able to do.

Here, I'm creating an ABC that merely marks other classes as all being 
"states", mostly for type checking purposes. I will create one 
@abstractmethod to indicate that any StateT subclass should have a 
ppstate() member method for pretty printing. StateT.ppstate() itself is 
not intended to ever run; it only raises an exception if a subclass 
does not implement its own ppstate(). The main purpose of an 
@abstractmethod is to tell Python that it should expect to find such a 
method in all classes that inherit from the ABC. It's even acceptable 
for a subclass to define an empty method in its place; so long as the 
author acknowledges that some definition for ppstate() was expected. 
(This is "we're all adults here" again.)

All state classes that inherit from StateT will produce objects for 
which isinstance(obj, StateT) will return True, and that's what I'm 
really after. This allows us to meaningfully express why non-terminal 
or working states might appear intermixed with terminal states, and 
gives an indication of what we intend to do in common with them - to 
print them as though they are the same type of thing.

StateT.ppstate() is entirely superfluous - I could do about the same 
thing with only __str__(). But I wanted something to demonstrate 
@abstractmethod, because abstract methods are the real purpose of 
abstract base classes - not just to create an empty class for a type 
checking shortcut. (The shortcut is viable too I just didn't want you 
to think that's all that the abc module is about.)
"""

class WorkingStateT(StateT, tuple):

  def __new__(cls, hand, card):
    return super().__new__(cls, (hand, card))
    
  def __repr__(self):
    return f'WorkingStateT({self[0].__repr__()}, {self[1].__repr__()})'
    
  def __str__(self):
    return f'{self[0]}, {self[1]}'
    
  def ppstate(self):
    return f'{self[0]}vs{self[1]}'
 
"""Python uses mechanisms like this under the hood to represent the 
commonalities in types with related meanings and shared operations, but 
different underlying representations - the rational numbers, 
floating-point numbers and decimal-precision numbers are a good
illustration of this. You can browse the Python docs on Numeric types 
for more context.

I could have written this same implementation without type checking or 
deriving subtypes. You will find I don't actually use StateT for any 
type checks - it predominantly expresses a conceptual relationship 
between the two concrete classes that inherit from it.

I may find either a WorkingStateT or TerminalStateT value in some 
places. But I know that's where StateT should be, and I usually want to 
differentiate between the two of them when I do, so I have limited use 
for the StateT name for the needs of this particular lab task. Because 
all of my valid values can be pre-calculated as finite collections of 
existing objects, I can use membership testing like 'if foo in bar:' 
rather than checking the Python type of each foo.

That's why most of my class declarations are about printable 
representation. A lot of useful behavior already exists in simple value 
types I base them on. And an empty class declaration creates plenty of 
useful behavior in and of itself just by adding a new type 
relationship. By focusing on trimming each class to a single idea or 
responsibility that it does very well, we can bring rich behavior to 
the surface with relatively simple ingredients.

There are probably more new types here than any of you used in your lab 
submissions, but I bet these are also some of the easiest classes to 
verify behavior on. After all, we are hardly changing anything; if the 
underlying behavior of str or int stopped working, we would have bigger 
problems than just this file.
"""
    
STATES_PRODUCT = frozenset(product(PLAYABLE_HANDS, CARDS))
CURLY_S = frozenset(WorkingStateT(*state) for state in STATES_PRODUCT)
  
class ActionT(str):

  def __repr__(self):
    return f'ActionT({self})'
    
  def __str__(self):
    return super().__str__()
    
STICK = ActionT('STICK')
HIT = ActionT('HIT')
CURLY_A = frozenset({STICK, HIT})
# Curly braces with key: value pairs are dictionaries, but curly braces 
# with just a series of objects specifies a set. Getting a frozenset 
# instance still requires a call to its constructor - and to construct 
# an empty set for either requires a call to their constructor set() 
# or frozenset().
SA_PAIRS = frozenset(product(CURLY_S, CURLY_A))

"""(21, HASACEVAL) and (21, NOACEVAL) don't quite describe all the 
terminal states. For one, they are only hands - they don't incorporate 
the dealer's showing card or hidden total, which do meaningfully 
describe portions of the underlying environmental model elsewhere.

A terminal state occurs when the player busts or sticks; at that point, 
there are no more actions possible in an episode and the resulting 
state can no longer change.

The win condition is then whether or not the player's score is greater 
than the dealer's score (but not greater than 21) after the dealer 
finishes their play. 21s are automatic wins - there is nothing the 
dealer can do to beat them at that point - but the hand alone doesn't 
describe the set of terminals well.
"""

class TerminalStateT(StateT, str):

  def __repr__(self):
    return f'TerminalStateT({self})'
    
  def __str__(self):
    return super().__str__()
    
  def ppstate(self):
    return str(self)
    
WIN = TerminalStateT('WIN')
DRAW = TerminalStateT('DRAW')
BUST = TerminalStateT('BUST')
TERMINAL_S = frozenset({WIN, DRAW, BUST})
CURLY_S_PLUS = CURLY_S | TERMINAL_S

"""I wrote addtohand() before defining actions at first, but both it 
and bigP() didn't make sense until I distinguished the terminal states.
"""

def addtohand(hand, newcard):
  """Adds newcard to the score value of hand and checks for aces.
  
  May return a hand that's not in the set of valid hands. Check results 
  against PLAYABLE_HANDS or CURLY_S to see if the addition resulted in 
  busting.
  """
  score, hasace = hand
  hadace = hasace
  if newcard == ACE:
    hasace = HASACEVAL
  
  score = ScoreT(score + newcard)
  if score > TWENTYONE and hasace:
    score = ScoreT(score - 10)
    hasace = hadace

  return HandT(score, hasace)
  
"""If we wanted we could override integer addition on CardT and ScoreT 
to automatically return ScoreT. And this might be a good idea if we 
were building a module that others would use to create custom blackjack 
environments. But it suffices that both CardT and ScoreT turn into 
primitive ints when we add them - if we find an int where we expect one 
of our derived types, it tells us we performed some integer-based 
operation without thinking about what the result should represent, and 
we can look for those kinds of oversights when tracing what part of the 
code set the poorly formed value.

We could even potentially override addition on hands so that we could 
use the plus operator to add cards. This would be bordering on bad data 
design and Python style, though. The plus operator should only ever be 
used to represent forms of numeric addition; to do otherwise may create 
false expectations for end users. It is not uncommon to find 
third-party modules that do not abide by this rule - especially ones 
that bind libraries from other languages, like how the Python OpenCV 
module is a wrapper for a C++ library.

Your mileage may vary. I think that the Python community makes a fair 
argument - that addition suggests that an operation has properties such 
as symmetry and commutativity.

Of course the Python language itself breaks this idea pretty directly; 
you can use '+' to catenate lists and strings and other Sequence types. 
List catenation is not symmetric, distributive nor commutative - it 
really isn't even close to an algebraic addition. But one of the things 
that made C++ so shiny back in the day was convenient string 
operations, so a lot of languages today provide syntactic sugar like 
'+' catenation. Even careful design tends to admit a few dinosaurs.

It's worth noting that, under the hood, some magic methods responsible 
for operators are used in surprising ways. You really should never 
override the related dunders for equality, greater than, less than, 
etc. because Python will automatically generate the ones you don't 
supply based on the ones you do, assuming that they represent a numeric 
ordering. Overriding '<=' as a convenient syntax to suggest an "arrow" 
will have unintuitive side effects that may not be immediately obvious.

Namely, if you were try to compare or automatically sort a class with 
an overriden __lte__() dunder, you'll find Python calling __lte__() a 
lot for no apparent reason as it tries to use whatever you wrote to 
represent numeric comparison. The interpreter will probably wildly 
misuse whatever value your custom method returns thinking the 
truthiness of the return value means something mathematical about your 
class instances. If this warning stresses you out, rest assured that it 
will never happen so long as you're mindful of magic methods and their 
responsibility in making Python work properly behind the scenes. 
They're overridable for a reason - we often need to change them - but 
they're also marked as special for a reason. They aren't made available 
for frivolity or playfulness.

If you want a high-level language that encourages playfulness, Ruby is 
great and play jives with its design ethos. Python is scientifically 
oriented, on the other hand - it leans hard on conventions and trusts 
that you know what you're doing if you break with them. Honestly I love 
Ruby for learning and prototyping and think it's a better language in 
many important regards. But the power of Python's structure (and its 
more robust ecosystem) won me over. I don't see myself ever coming back 
to Ruby as my daily driver so long as Python is also an option. It's 
been well worth my time to adjust my style to the Python community - 
it's paid dividends and I'm not even in the workplace yet.
"""

def playto(value, hand):
  """Adds cards to a hand until its score meets or exceeds value.
  
  May return a HandT that is not in CURLY_S.
  """
  while True:
    newcard = choice(CARD_DECK)
    hand = addtohand(hand, newcard)
    score, _ = hand
    if score >= value:
      break
  return hand
  
def newhand(firstcard=None):
  """Creates a new hand at random by drawing one or more cards.
  
  Does not return only the first deal - all hands are played up to the 
  first nontrivial score. Hands returned should be within CURLY_S - and 
  it should be possible to return any hand within CURLY_S. (I've been 
  wavering over whether or not a few configurations are possible to 
  play but not possible to receive as a starting hand.)
  """
  hand = EMPTY_HAND
  if firstcard is None:
    firstcard = choice(CARD_DECK)
  hand = addtohand(hand, firstcard)
  hand = playto(min(NONTRIVIAL_SCORES), hand)
  return hand
  
"""Cards are drawn until the hand reaches a non-trivial state space 
with a score or hand value of 12 (11?) or above.

This is preferable to choosing directly from the set of possible hands 
because it takes the probability of different face values into account.

Since we're adding the value of cards, the true probability 
distribution is not linear. (Sums of equiprobable random variables have 
distributions on a bell curve. Distributions of dice rolls are 
frequently used as an example of this if you want a visualization or 
demonstration.) Since cards with value ten are overrepresented, the 
distribution is also skewed. Randomly choosing from the set of possible 
states with even odds would not give us the same results as the 
(infinite) deck described in the problem.

I can demonstrate alternate strategies if there is interest. Computing 
the space of all card combinations - not just their values - is one. 
Calculating the exact probability distribution, and mapping it onto the 
states represented as values and availability of an ace, is another.
"""

def dealerplay(state, stickval=17):
  """Finishes the episode after a stick by playing the dealer's hand.
  """
  if state in TERMINAL_S:
    return state
  hand, dealercard = state
  if hand in WINNING_HANDS:
    return WIN # It's possible to win before the dealer can act
  score, _ = hand
  
  dealerhand = newhand(dealercard)
  dealerhand = playto(stickval, dealerhand)
  dealerscore, _ = dealerhand
  
  if score > dealerscore or dealerhand not in PLAYABLE_HANDS:
    return WIN
  elif score == dealerscore:
    return DRAW
  else:
    return BUST

"""Blackjack is a fairly simple game of chance, but the combinatoric 
properties of decks of cards have very complex math attached even when 
the rules are otherwise basic. By assuming an infinite deck we simplify 
the odds of drawing a given value of card quite a bit. But the fact 
that we could draw five twos before reaching the first non-trivial 
score of 11 - or reach it in a single draw with an ace - means that the 
odds of each hand, and the odds of each starting state, are now a 
combination of many sizes of hand, and the limitation on going over 21 
creates an irregularity in the shape and probability of playable 
states.

As a result, it would be a challenge to fully tabulate the MDP 
transition function for blackjack, probably beyond the scope of this 
exercise too. And I believe that's one point that Sutton and Barto are 
trying to convey somewhere around this chapter - that some problems 
have inconvenient characteristics for modeling even when you know quite 
a lot about them on paper. For problems of certain forms, we can 
succeed without the need for a detailed model in software.

For those curious, an approach to implement a tabular method would be 
to factor out the random trials in the various helper functions and 
instead provide those values as function parameters. This would entail 
refactoring the loops as well - perhaps to take sequences of cards 
rather than one at a time, or to rewrite those methods in terms of a 
single iteration. The FiniteDistribution.mixture() method in some of my 
earlier examples would be the basis for this approach.

By separating the random and iterative portions of the algorithm we can 
quantify the portions that have a probabilistic impact on the 
determination of state, which can then be combined with the 
card-drawing odds in a quantifiable, proportionally sensible way. From 
there it would be possible to create weighted tabulations of the 
respective probabilities, but it seems like it could be grueling.

I tried to determine termination in the transition function alone at 
first, but the fact of the matter is that addtohand() can put us into 
a terminal state all by itself, before you even consider sticking and 
letting the dealer make a play. As a result there are at least three 
places to determine a potential win or other terminal state; as the 
player receives their hand, when the player adds a card to their hand, 
and as the dealer resolves play (which itself might be seen as having 
two choice points - the dealer not busting, and the dealer beating the 
player's score.)
"""

def bigP(state, action):
  hand, dealercard = state
  
  if action == HIT:
    newhand = addtohand(hand, choice(CARD_DECK))
    if newhand in WINNING_HANDS:
      return WIN
    elif newhand not in NONTRIVIAL_HANDS:
      return BUST
    else:
      return WorkingStateT(newhand, dealercard)
  else:
    return dealerplay(state)

"""Rewards for MDPs are always defined as members of the real numbers, 
so float is a sufficient representation. If there were some chance of 
mistaking a reward for a q value we might implement one or both as 
their own subclass of float, but we don't need to test a q value or 
reward for type in any of our algorithms.

You could possibly say the same for card values and hand scores, and 
again I'll stress that this implementation is completely doable with 
only primitive types and little to no type checking. But distinguishing 
CardT ints from ScoreT ints allows us to differentiate them both 
programmatically and in our pretty prints.

On the other hand, it's easy to tell the difference visually between 
whole-valued rewards and q values, which tend to have many digits of 
precision unless they're zero. It's also unlikely a user would mix the 
two up because no methods use them as inputs, whereas a user might 
misunderstand how to create a hand or non-terminal state and use a 
CardT value where a ScoreT is expected.
"""

WINREWARD = 1.0
LOSEREWARD = -1.0
NEUTRALREWARD = 0.0
CURLY_R = frozenset({WINREWARD, LOSEREWARD, NEUTRALREWARD})

# bigR is functional (has no side effects) so we can make use of the 
# cache decorator
@cache
def bigR(state):
  if state == WIN:
    return WINREWARD
  elif state == BUST:
    return LOSEREWARD
  else:
    return NEUTRALREWARD
    
"""Lambdas are little functions that don't have a name on their own. 
And, in Python, functions are just objects with the special method 
__call__() defined on them. A lambda statement returns a function with 
no name, but if you assign it to the variable var, you can call it with 
var(). Lambdas are convenient for very simple functions, especially 
when you only need the function to tell another function what to do.
"""

eqrandpi = lambda _: choice(CURLY_A)

def score(state):
  hand, _ = state
  score, _ = hand
  return score
  
"""A function can return another function. Then you can save that value 
and use it elsewhere. stickon() creates functions that represent the 
policy that sticks on a given value. The return value is then a policy 
that we can give to our episode evaluator. It satisfies the definition 
of a policy because it is a function or mapping from all the states in 
the MDP problem definition as curly S, onto one of the actions found in 
the corresponding available actions curly A subscript s:

policy: CURLY_S -> CURLY_A
such that a is an element of CURLY_A_SUB[s] for all (s, a) in pi

Or in slightly closer to Python:

policy: Callable[StateT, ActionT]
all(a in CURLY_A_SUB[s] for s, a in pi)
"""

def stickon(value):
  return lambda s: HIT if score(s) < value else STICK

stickon17pi = stickon(ScoreT(17))
stickon20pi = stickon(ScoreT(20))
  
"""Generators are an important part of Python that you may not have 
come across. Javascript/ECMAscript and their derivatives have similar 
features, as do Ruby, C# and PHP. Generators implement one variety of 
lazy evaluation.

When you call a generator, you do not immediately get the results of 
that method. What you get is an object that represents that bit of 
code as it is about to run.

The object acts like an iterator, meaning that you can get one result 
out of it at a time like a collection. With a Sequence, you can 
subscript the container with an integer value and browse the contained 
items in any order. Iterators don't have an "order" though, so you 
can't subscript them. They only promise to know how to try to find 
"another" or "the next" of whatever they contain or - in this case - 
generate. They don't allow you to specify "which one".

Whenever you call the built-in method next() on a generator object, the 
code resumes and runs until it hits a yield statement, and then returns 
the value in the yield statment. The interesting part is that the 
generator object then saves its place in the code, and will resume 
there with the same state the next time a value is requested from the 
generator object with next().
  
Generators have their own variables that maintain persistent state 
between calls to next(). They also have access to any variables in 
their definition from an outside scope. A consequence of this is that 
generators are also a kind of "closure", meaning a representation of an 
algorithm/calculation along with its environment or data context.
  
Here's some trivia: were you aware that str is a Sequence in Python? 
"abc"[0] will return the character 'a'. (Which, confusingly enough, is 
both a single character and a string, and therefor itself a Sequence. I 
recently noticed this by infinitely recursing into a list of lists that 
also occasionally contained strings.)
"""

def isstateactionpair(obj):
  ispair = (isinstance(obj, tuple) and
            isinstance(obj[0], WorkingStateT))
  return ispair

def episode(pi, start):
  """Generator function that yields the states in an episode.
  
  The final value will be the terminal state encountered.
  """
  if isinstance(pi, Mapping):
    policy = pi.get
  else:
    policy = pi

  match start:
    case (WorkingStateT(_) as s, ActionT(_) as a):
      state = s
      action = a
    case WorkingStateT(_):
      state = start
      action = policy(state)
    
  while True:
    newstate = bigP(state, action)
    yield state, action, bigR(newstate)
    state = newstate
    if state in TERMINAL_S:
      break
    action = policy(state)
  yield state, None, None
  
"""Generators can't be indexed/subscripted, but they can be unpacked 
into lists and other sequence types, so long as we know that the 
generator will eventually terminate. And if we aren't sure about that, 
we can just take a finite amount of elements using a slice or list 
comprehension instead of trying to gobble down the whole potentially 
infinite thing. The itertools module also has helpers that will wrap an 
infinite generator and evaluate just a part of it.

Our problem can be expressed conveniently with generators because it 
has definite termination and we can show that it will always terminate. 
We know it will terminate because your hand will eventually fill and 
reach an end condition even if you only draw low value cards; aces can 
go from being worth 11 to one, but they're still worth at least one. 
You must draw a card or choose to end the game, and you can only draw 
at most 21 cards before busting.

First-visit Monte Carlo evaluation is an algorithm that does not 
terminate. Generators shine here too! Monte Carlo evalutaion creates a 
series of value estimates and updates them in a recurrence 
relationships - that's like an iterator, so we can use a generator to 
express it.

This one is kind of spicy. It can evaluate values per state or 
state-action pair, depending on what starting conditions it receives. 
It accepts different collections of states so that it can be exploring 
starts, equiprobable random starts, etc. It accepts a function to 
initialize the value estimates, so that they can be initialized with a 
constant, randomly generated values, or even based on their state or 
state-action key in the value dictionary. Both first-visit and 
every-visit are supported.

And because it is a generator it can run forever - you can just keep 
asking for the next() iteration of the value dictionary, and you decide 
when it's converged enough. All the stateful details of executing the 
algorithm are inside the generator object that is returned when you 
first call montecarloevaluation().
"""

ZEROVALFUN = lambda _: 0.0
def montecarloevaluation(
  pi, 
  startingstates,
  gamma=1.0,
  valinitfun=None, 
  firstvisits=True
):
  start = next(startingstates)
  if isinstance(start, WorkingStateT):
    space = CURLY_S
  else:
    space = SA_PAIRS
    
  bigV = {}
  if valinitfun is None:
    valinitfun = ZEROVALFUN
  for key in space:
    bigV[key] = valinitfun(key)
    
  returns = {state: (0.0, 0) for state in space}
  # Why yield already? So that we know the starting state of the 
  # estimates. We could call with 'valinitfun=lambda _: random()' for a 
  # random number between 0.0 and 1.0, for instance, and it'd be nice 
  # to know what those random starting values were.
  yield bigV, []
  while True:
    episodetuples = list(episode(pi, start))
    bigG = 0.0
    visited = set()
    # The terminal state at episode[-1] has no corresponding action or 
    # reward, so we will take the slice of episode up to the final 
    # tuple - also known as the "init" or "initials" of the list in 
    # functional programming terms. We then reverse the init to 
    # iterate the states in reverse order.
    for state, action, reward in reversed(episodetuples[:-1]):
      bigG = gamma * bigG + reward
      if space == SA_PAIRS:
        key = (state, action)
      else:
        key = state
      if not firstvisits or key not in visited:
        sum_, visitcount = returns[key]
        sum_ = sum_ + bigG
        visitcount = visitcount + 1
        returns[key] = sum_, visitcount
        bigV[key] = sum_ / visitcount
      visited.add(key)
    yield bigV, episodetuples
    start = next(startingstates)

"""The algorithm calls for storing a list of returns per state, but the 
only time we will use returns[state] is to call sum(returns[state]) and 
divide by len(returns[state]). I choose to keep a running total and 
denominator explicitly, because the list doesn't really get us 
anything.

I made this same choice when I implemented this as a student, but after 
a couple years really drilling on design books I understand better just 
why I felt it was right.

If we ran for so long that the variable overflows, storing the summands 
in an ever-growing list still wouldn't fix the overflow in the eventual 
sum that comes before averaging. You'd have to fix the types used one 
way or the other, but only one approach requires you to eat memory 
dynamically before the overflow bug even occurs.

Don't prematurely optimize! Wait for the bug to actually show itself!
"""

def randomstate():
  return WorkingStateT(newhand(), choice(CARD_DECK))

def eqrandomstate():
  return choice(list(CURLY_S))
  
"""Are you wondering how to run a potentially infinite number of 
episodes with a pre-defined collection of startingstates? Here's how:
"""

RANDOMSTARTSTATES = map(lambda _: randomstate(), repeat(None))
EQRANDOMSTARTSTATES = map(lambda _: eqrandomstate(), repeat(None))

"""repeat(obj) with no second parameter produces a generator that 
repeats the object forever. map(fun, iter) produces a generator that 
applies the function fun() to objects from the iterable iter. If the 
iterable is endless, like an infinite generator, the resulting map (not 
the same as a Mapping) object will be an infinite series of calls to 
the function.

It all happens lazily, so one call is only ever made at a time, but 
they have no definite end - you can keep taking values forever. None of 
the values are stored in memory unless you save them to a variable - 
they just pour out of the generator and evaporate unless you bottle 
them. Handy for tasks like this where you may want to search for 
trillions of iterations. You can't do that with a list.

These generators allow us to customize the behavior for choosing the 
starting state of each iteration of Monte Carlo evaluation. 
RANDOMSTARTSTATES() and EQRANDOMSTARTSTATES() both generate an infinite 
series of states, and we can pass any of them to startingstates to 
customize our Monte Carlo episode sampling.

We have a partial model for blackjack, but we don't have the explicit 
probabilities. The authors solve this with exploring starts - 
specifying the states and actions for the first step of the episode, 
not just the starting state.

I went back and modified episode() so that the start parameter can be a 
state or a tuple - in which case it's interpreted as a state-action 
pair. Then a little work was needed to help the evaluation function 
know how to record the associated value estimates. But overall it was 
wasn't significantly more effort than it would have been to copy the 
form of my state-based version and rewrite it specific to state-action 
pairs. In the process I was able to make the same function capture 
several different variations of evaluation, all with the same bit of 
code.

Or maybe I misread the book and should have skipped directly over state 
evaluation. I've got a lot on my plate.
"""

def randomstateaction():
  return randomstate(), choice(list(CURLY_A))

def eqrandomstateaction():
  return eqrandomstate(), choice(list(CURLY_A))

RANDOMSTARTPAIRS = map(lambda _: randomstateaction(), repeat(None))
EQRANDOMSTARTPAIRS = map(lambda _: eqrandomstateaction(), repeat(None))

"""On-policy Monte Carlo control is implemented with regard to 
epsilon-soft policies and yields greedy policies at each improvement 
step. I'll present an alternative strategy to the FiniteDistribution I 
used in the last lab.
"""

def epsilonpi(pi, epsilon):
  def epi(state):
    if epsilon > random():
      return choice(CURLY_A)
    else:
      return pi(state)
  epi.epsilon = epsilon
  return epi

"""For the purposes of Monte Carlo control, it is sufficient to have 
exploratory actions equiprobable. And the chance of making an 
exploratory action is the same regardless of state. We can simply wrap 
the original policy function with a random chance of exploring.

Monte Carlo control needs to know what epsilon value was used in order 
to taper that value as estimate accuracy improves. Because functions 
are objects, we can record the epsilon value as an attribute before 
returning the wrapped policy function. Then our Monte Carlo control 
implementation can look for pi.epsilon to get the relevant amount - and 
if the passed policy pi doesn't have an epsilon attribute, we know the 
user might not have correctly understood the calling conditions of the 
function.

We can write any sort of function to represent our policy to begin 
Monte Carlo exploration. But we can also create a piecewise mapping 
like a dictionary to serve as our policy.
"""

def greedypi(qvs):
  pi = {}
  for s in sorted(CURLY_S):
    qvsbya = lambda a: qvs[s, a]
    pi[s] = max((a for a in CURLY_A if (s, a) in qvs), key=qvsbya)
  return lambda s: pi[s]
  
"""I think I meant to write more about evaluation and policy 
improvement here, but I'm a little short on time and want this to be 
available for reference. If there's interest, I may add more from here.
"""

pass
    
"""The basic __repr__()s provided for each fundamental type create 
pretty chunky output that is basically unreadable for the purposes of 
printing a whole value dictionary/matrix. So I'll create a few pretty 
printers for common views.

I can make use of strongly typed values to put behavior for multiple 
types into the same pretty printer.

Pretty printers are not a part of the lab assignment, so I'm granting 
myself some latitude to be weird and messy beyond this point, for the 
sake of providing tools to examine the rest of the code. In a real code 
module, I would hide some of these objects from users with the __all__ 
special attribute - which determines what does (and doesn't) get 
imported when using 'from <module> import *'. Many constants I derive 
here don't mean anything to the problem or users of the module, they're 
just to help me size the output of the pretty printer.

One can still import objects that are not in a module's __all__ list, 
but it is taken as a convention for expressing which objects the author 
did (and didn't) intend for outside use.
"""

CARD_STR_LEN = 2 + max(len(str(card)) for card in CARDS)
SCORE_STR_LEN = 2 + len(str(TWENTYONE))
HAND_STR_LEN = 2 + max(len(str(hand)) for hand in PLAYABLE_HANDS)
STATE_STR_LEN = 2 + max(len(str(state)) for state in CURLY_S_PLUS)
ACTION_STR_LEN = 2 + max(len(str(action)) for action in CURLY_A)

def ppcard(card):
  return f'[{str(card)}]'.center(CARD_STR_LEN - 2, '|')
  
def ppscore(score):
  return '{' + str(score).rjust(SCORE_STR_LEN - 2) + '}'
  
def pphand(hand):
  return '/' + str(hand).ljust(HAND_STR_LEN - 1, '/') 

def ppworkingstate(workingstate):
  return '..' + workingstate.ppstate().ljust(STATE_STR_LEN - 2, '.')

def ppterminalstate(terminalstate):
  return terminalstate.ppstate().center(STATE_STR_LEN, '-')
  
def ppaction(action):
  return action.center(ACTION_STR_LEN, '_')

def ppstateactionpair(sapair):
  state, action = sapair
  return f'{ppstr(state)}->{ppstr(action)}'

SAPAIR_STR_LEN = 2 + STATE_STR_LEN + ACTION_STR_LEN

QVALUE_MAGNITUDE = 4 # From -1,000 to +1,000
QVALUE_PRECISION = 4 # ...with four decimal places
# Plus one character for the sign and one for the decimal point
QVALUE_STR_LEN = 2 + QVALUE_MAGNITUDE + QVALUE_PRECISION

def ppqvalue(qv):
  return f'{qv:+{QVALUE_STR_LEN}.{QVALUE_PRECISION}f}'

"""Python match statements look like switch or case blocks from other 
languages, but there's a lot more going on and they probably don't work 
how you would expect. Python match is modeled after pattern matching in 
logical or functional programming languages. The object is not compared 
for equality but rather is unpacked into the form described in each 
case. Thus, cases are not objects for comparison but rather prototypes 
that describe forms we expect the object to take.

A case is satisfied if obj can be structurally matched to it; if an 
object equal to obj can be created as 'CardT(val)', then the first case 
below will match and ppcard(obj) will be called. Structural pattern 
matching is a relatively new feature and I don't know its full extents;
I believe it might rely on the objects being value types.
"""

def ppstr(obj):
  match obj:
    case CardT(val):
      # If we wanted, we would have access to the card's value in this 
      # scope as 'val'
      return ppcard(obj)
    case ScoreT():
      # Another option is to not capture the value and use an empty 
      # constructor
      return ppscore(obj)
    case HandT():
      return pphand(obj)
    case WorkingStateT():
      return ppworkingstate(obj)
    case TerminalStateT():
      return ppterminalstate(obj)
    case ActionT():
      return ppaction(obj)
    case (WorkingStateT(), ActionT()):
      return ppstateactionpair(obj)
    case (WorkingStateT() as s, float() as qv):
      return f'{ppworkingstate(s)}: {ppqvalue(qv)}'
    case ((WorkingStateT(), ActionT()) as sa, float() as qv):
      return f'{ppstateactionpair(sa)}: {ppqvalue(qv)}'

"""Tuple values are sorted from their left-most member onward, not 
unlike how the first digit of a number represents the most significant 
amount. That means that WorkingStateT objects sort with HasAceT values 
interleaved per hand score by default. This can make it hard to see how 
a given hand score lines up with a given shown dealer card, as all the 
combinations of dealer cards for the given score-ace pair are between 
that state and the equivalent state with or without a usable ace.

We can provide a key function that swaps the order of items in a tuple 
to swap the order they are considered in by methods like sorted(), 
max() and min() which accept an optional key parameter.
"""

def statekey(state):
  (score, hasace), card = state
  return score, card, hasace

def sapairkey(sapair):
  state, action = sapair
  return statekey(state), action

"""Estimating values for just states doesn't make sense for this 
problem, but conceivably I might come back and try to lift some of this 
code without remembering the constraints of this lab. So I've tried to 
build things for the general parameters of MDP problem definitions and 
policies as much as possible, as with the following pretty printer for 
q value dictionaries.

If it's states only, we may have made a mistake, but we can convert the 
q values to state-action pairs trivially by providing the original 
value of the state at each pair. This should only work in the pretty 
printer, because if a user wanted to convert state values to 
state-action values meaningfully, it would imply some sort of neighbor 
averaging or another approach specific to the mechanics of states and 
the environment. Misleading behavior in a pretty printer is relatively 
benign so we can be a little less careful here.
"""

def ppsaqvalues(qvdict):
  if isstateactionpair(list(qvdict.keys())[0]):
    qvs = {s: {} for s, _ in qvdict}
    for s, a in qvdict:
      qvs[s][a] = qvdict[s, a]
  else:
    qvs = {s: {} for s in qvdict}
    for s in qvdict:
      for a in CURLY_S:
        qvs[s][a] = qvdict[s]
  
  qvstrings = {}
  for s in sorted(qvs):
    string = ppstr(s)
    for a in sorted(CURLY_A):
      if a in qvs[s]:
        string = string + ppqvalue(qvs[s][a])
      else:
        string = string + '(no val)'.center(QVALUE_STR_LEN, '!')
    qvstrings[s] = string
  return qvstrings
      
"""Avoid double dictionaries unless you're doing something very simple 
with them and a dataclass or namedtuple is not sufficient to represent 
the structure of the values stored in the top-level dictionary. It's 
generally considered preferable to create a class or wrapper function 
that makes the meaning of stored values clear, rather than permitting 
any dictionary to represent a composite object and leaving it up to the 
reader/user to figure out what qualities those dictionaries must have 
for your code to work as expected.

I got distracted working on the pretty printer. I had to put this down 
and when I came back I couldn't remember what I intended to show in 
terms of driving this code. Your loss is my gain, because I'm leaving 
this as an exercise for the reader - sorry folks, I'm busy. But it 
would be pretty much the same as what I walk though at the end of 
lab4.py, so I encourage you to work through that one first if you 
haven't already.

Apply the same ideas here - use interactive Python to look at the 
different constants, make some instances of the types, etc. Take a look 
at the episode() generator function and see how it generates a list of
state transitions one time step at a time. If there's interest I'd be 
happy to walk through this another time for lecture or a study session.

I'm confident I can place this in your hands - do your best.

~Joe

Key references:
https://peps.python.org/pep-0008/
https://peps.python.org/pep-0257/
https://peps.python.org/pep-0484/
https://docs.python.org/3/
https://docs.python.org/3/tutorial/interpreter.html#interactive-mode
https://github.com/psf/black
Ramalho, Luciano. 2015. Fluent Python: Clear, Concise and Effective 
  Programming. O'Reilly.
Gamma, Erich et al. 1994. Design Patterns: Elements of Reusable Object-
  Oriented Software. Addison-Wesley.
Martin, Robert Cecil. 2009. Clean Code: A Handbook of Agile Software 
  Craftsmanship.
"""

"""To do:
- Switch isstateactionpair() to structural matching
- Implement behavior around epsilon soft policy methods
- Is it possible to start with (21, NoAce)? Can't decide
"""