import random
from tabulate import tabulate

card_list = [1,2,3,4,5,6,7,8,9,10,10,10,10]
def draw_card():
    return random.choice(card_list)

class Hand:
    def __init__(self):
        self.score = 0
        self.turn = 0
        self.usable_ace = False
        self.playing = True
        self.bust = False
    def hit(self):
        card = draw_card()
        if card == 1 and self.score < 11:
            self.score += 11
            self.usable_ace = True
        else:
            self.score += card
        if self.score > 21:
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

class Agent:
    def __init__(self):
        self.episodes = []
        self.states = {}
        self.new_episode()
    def new_episode(self):
        self.episode = []
        self.hand = Hand()
        self.hand.hit()
        self.hand.hit()
        self.dealer = Dealer()
        while self.hand.score < 12:
            self.hand.hit()
        state = self.State(self.hand.score, self.dealer.show, self.hand.usable_ace)
        self.episode.append(state)
        if state.state_id() not in self.states:
            self.states[state.state_id()] = state
        else:
            self.states[state.state_id()].visited += 1
    def play_hand(self):
        while self.hand.playing:
            if self.hand.score < 20:
                self.hand.hit()
            else:
                self.hand.stick()
            state = self.State(self.hand.score, self.dealer.show, self.hand.usable_ace)
            if state.state_id() not in self.states:
                self.states[state.state_id()] = state
            else:
                self.states[state.state_id()].visited += 1
            self.episode.append(self.states[state.state_id()])
        self.end_episode()
    def end_episode(self):
        # 0 = Draw, -1 = Lose, 1 = Win
        reward = 0
        if self.hand.bust:
            reward = -1
        elif self.hand.score < self.dealer.hand.score and not self.dealer.hand.bust:
            reward = -1
        elif self.dealer.hand.bust or self.hand.score > self.dealer.hand.score:
            reward = 1
        for i in range(len(self.episode) - 1, -1, -1):
            state = self.episode[i]
            ot = state.estimate * (state.visited - 1)
            state.estimate = (ot + reward) / state.visited
        self.episodes.append(self.episode)
        self.new_episode()
    class State:
        def __init__(self, score, upcard, ace):
            self.score = score
            self.usable_ace = ace
            self.upcard = upcard
            self.visited = 1
            self.estimate = 0.0
        def state_id(self):
            return (self.score, self.upcard, self.usable_ace)

agent = Agent()
while len(agent.episodes) < 1000:
    agent.play_hand()
vals = []
for s in agent.states.values():
    vals.append([s.score, s.upcard, s.usable_ace, round(s.estimate, 2), s.visited])
vals.sort(key=lambda x: (x[0], x[1]))
print(tabulate(vals, headers=['Hand', 'Upcard', 'Ace', 'Estimate', 'Visited']))
