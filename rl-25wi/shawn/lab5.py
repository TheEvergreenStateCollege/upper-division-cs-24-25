#!/bin/python3
import sys # For reading cli arguments
import random # For drawing cards
from tabulate import tabulate # For pretty printing of policy

# Group:
# Shawn Bird
# Austin Strayer
# Hayden Edge
# Dawson White

## RL Lab 5
## Goals: understand Monte Carlo simulation, in particular Blackjack
## Task: program the simulation in Python, where the agent and the 
## environment are distinct. The agent estimates the value of a state
## by averaging the returns using first visit.
## A state is the sum of values in a hand plus the value of the 
## dealer's card showing plus whether there is a usable ace.
## There are about 200 states.
## 1. build the environment
## 2. build a simple agent
## 3. collect data
## Work in groups and make sure to include the names of the members in your group

# Create a list of possible card draws, a 10 for each face card
card_list = [1,2,3,4,5,6,7,8,9,10,10,10,10]
def draw_card():
    return random.choice(card_list)

# Hands hold the state relative to the player. Agents will have a hand and so will the dealer
# The hit() and stick() methods allow the hand to be played
class Hand:
    def __init__(self):
        self.score = 0
        self.turn = 0
        self.usable_ace = False
        self.playing = True
        self.bust = False
    def hit(self):
        card = draw_card()
        # Handle aces
        if card == 1 and self.score < 11:
            self.score += 11
            self.usable_ace = True
        else:
            self.score += card
        # Handle busts
        if self.score > 21:
            # Use an ace to prevent busting when possible
            if self.usable_ace and self.score < 32:
                self.score -= 10
                self.usable_ace = False
            else:
                self.bust = True
                self.playing = False
        self.turn += 1
    def stick(self):
       self.playing = False
       self.turn += 1

# Dealer class to hold dealer behavior
# By default the dealer will hit until they have a score of 17 or more
class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.hand.hit()
        self.show = self.hand.score
        self.hand.hit()
        while self.hand.score < 17:
            self.hand.hit()
        else:
            self.hand.stick()

# Class to hold the agent, including episodes and states
class Agent:
    def __init__(self):
        self.episodes = []
        self.states = {}
        self.new_episode()
    # Episodes are used to segment hands
    # new_episode() resets the hand and hits until a score of 12 or more
    def new_episode(self):
        self.episode = []
        self.hand = Hand()
        self.hand.hit()
        self.hand.hit()
        self.dealer = Dealer()
        # It's always better to hit with a score below 12, so it's done automatically
        while self.hand.score < 12:
            self.hand.hit()
        # Update starting state in policy and add it to the episode
        state = self.State(self.hand.score, self.dealer.show, self.hand.usable_ace)
        if state.state_id() not in self.states:
            self.states[state.state_id()] = state
        else:
            self.states[state.state_id()].visited += 1
        self.episode.append(state)
    def play_hand(self):
        # By default the agent will hit until reaching a score of 20 or greater
        # More complex agent behaviour should go here
        while self.hand.playing:
            if self.hand.score < 20:
                self.hand.hit()
            else:
                self.hand.stick()
            # Add to the visited counter for each state reached, starts at 1
            state = self.State(self.hand.score, self.dealer.show, self.hand.usable_ace)
            if state.state_id() not in self.states:
                self.states[state.state_id()] = state
            else:
                self.states[state.state_id()].visited += 1
            self.episode.append(self.states[state.state_id()])
        self.end_episode()
    def end_episode(self):
        # Calculate the reward
        # 0 = Draw, -1 = Lose, 1 = Win
        reward = 0
        # Busting always results in a loss
        if self.hand.bust:
            reward = -1
        # Getting a lower score than the dealer also results in a loss
        elif self.hand.score < self.dealer.hand.score and not self.dealer.hand.bust:
            reward = -1
        # If the dealer busts or has a lower score it results in a win
        elif self.dealer.hand.bust or self.hand.score > self.dealer.hand.score:
            reward = 1
        self.episode[-1].outcome = reward
        # All other conditions result in a draw
        # Add the reward to the average for each state in the episode
        for i in range(len(self.episode) - 1, -1, -1):
            state = self.episode[i]
            ot = state.estimate * (state.visited - 1)
            state.estimate = (ot + reward) / state.visited
        self.episodes.append(self.episode)
        # Start the next episode and draw a fresh hand
        self.new_episode()
    # Class to hold the states used for calculating the policy
    class State:
        def __init__(self, score, upcard, ace):
            self.score = score
            self.usable_ace = ace
            self.upcard = upcard
            self.visited = 1
            self.estimate = 0.0
            self.outcome = 0
        def state_id(self):
            return (self.score, self.upcard, self.usable_ace)

hands = 100 # Default value
# Check first argument for custom number of hands
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    hands = int(sys.argv[1])

# Initialize the agent
agent = Agent()
# Play  hands
while len(agent.episodes) < hands:
    agent.play_hand()

vals = [] # To store the policy as a two dimensional array
# Load each state into vals
for s in agent.states.values():
    vals.append([s.score, s.upcard, s.usable_ace, round(s.estimate, 2), s.visited])

# Sort by ending score first, then by upcard
vals.sort(key=lambda x: (x[0], x[1]))
# Print the tabulated data with headers
print(tabulate(vals, headers=['Hand', 'Upcard', 'Ace', 'Estimate', 'Visited']))
print() # Blank line for spacing

# Count up the total wins, losses and draws then print them
wins = 0
losses = 0
draws = 0
for e in agent.episodes:
    if e[-1].outcome == 1:
        wins += 1
    elif e[-1].outcome == -1:
        losses += 1
    else:
        draws += 1
print("Wins: {0:3d} | Losses: {1:3d} | Draws: {2:3d}".format(wins, losses, draws))
