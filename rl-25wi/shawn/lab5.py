import random

card_list = [1,2,3,4,5,6,7,8,9,10,10,10,10]
def draw_card():
    return card_list[random.randint(0,12)]

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
    def next_turn(self):
        if self.hand.score < 17:
            self.hand.hit()
        else:
            self.hand.stick()

class Agent:
    def __init__(self):
        self.new_episode()
        self.episodes = []
    def new_episode(self):
        self.episode = []
        self.hand = Hand()
        self.hand.hit()
        self.hand.hit()
        self.dealer = Dealer()
        if self.hand.score < 12:
            self.hand.hit()
        state = self.State(self.hand, self.dealer.show)
        self.episode.append(state)
    def play_hand(self):
        while self.hand.playing:

            state = self.State(self.hand, self.dealer.show)
            self.episode.append(state)
        self.end_episode()
    def end_episode(self):
    class State:
        def __init__(self, hand, upcard):
            self.hand = hand
            self.upcard = upcard

agent = Agent()
while len(agent.episodes) < 1000:
    agent.play_hand()
