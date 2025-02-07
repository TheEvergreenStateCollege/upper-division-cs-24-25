import random

card_list = [1,2,3,4,5,6,7,8,9,10,10,10,10]
def draw_card():
    return card_list[random.randint(0,12)]

class Hand:
    def __init__(self):
        self.score = 0
        self.turn = 0
        self.hits = 0
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
            if self.usable_ace:
                self.score -= 10
                self.usable_ace = False
            else:
                self.bust = True
                self.playing = False
        self.turn += 1
    def stick(self):
       self.turn += 1
       self.playing = False

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
        self.new_episode()
        self.episodes = []
        self.states = {}
    def new_episode(self):
        self.episode = []
        self.hand = Hand()
        self.hand.hit()
        self.hand.hit()
        self.dealer = Dealer()
        while self.hand.score < 12:
            self.hand.hit()
        state = self.State(self.hand, self.dealer.show)
        self.episode.append(state)
    def play_hand(self):
        while self.hand.playing:
            state = self.State(self.hand, self.dealer.show)
            if state.state_id() not in self.states:
                self.states[state.state_id()] = state
            else:
                self.states[state.state_id()].visited += 1
            self.episode.append(self.states[state.state_id()])
            if self.hand.score < 20:
                self.hand.hit()
            else:
                self.hand.stick()
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
        def __init__(self, hand, upcard):
            self.hand = hand
            self.upcard = upcard
            self.visited = 1
            self.estimate = 0.0
        def state_id(self):
            return (self.hand.score, self.upcard, self.hand.usable_ace)
        def __str__(self):
            return "Hand: " + str(self.hand.score) + " |  Upcard: " + str(self.upcard) + " | Usable Ace: " + str(self.hand.usable_ace) + " | Estimate: " + str(round(self.estimate, 2)) + " | Visited: " + str(self.visited)

agent = Agent()
while len(agent.episodes) < 1000:
    agent.play_hand()
for s in agent.states.values():
    print(s)
