import random
import sqlite3
import string

AIUID = "WOPR"
EPSILON = 0.1
db = sqlite3.connect('data.db')
matches = {}

### Game Logic ###
class Match:
    def __init__(self):
        self.uidp1 = AIUID
        self.uidp2 = "TRAINER"
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.agent = Agent(self)
        self.boardID = 0
        
    def toMove(self):
        if self.board.count(1) > self.board.count(2):
            return self.uidp2
        return self.uidp1

    def currentTurn(self):
        return 10 - self.board.count(0)

    def boardState(self):
        return int(''.join(str(num) for num in self.board))

    def newMatch(self):
        characters = string.ascii_letters + string.digits
        matchID = "".join(random.choice(characters) for _ in range(5))
        while matchID in matches:
            matchID = "".join(random.choice(characters) for _ in range(5))
        return matchID

    def newBoard(self, matchID):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.agent = Agent(self)
        if self.toMove() == AIUID:
            self.submitTurn(AIUID, self.agent.nextMove())

    def checkWin(self):
        if self.board[0]:
            if self.board[0] == self.board[1] and self.board[0] == self.board[2]:
                return self.board[0]
            if self.board[0] == self.board[3] and self.board[0] == self.board[6]:
                return self.board[0]
            if self.board[0] == self.board[4] and self.board[0] == self.board[8]:
                return self.board[0]
        if self.board[1]:
            if self.board[1] == self.board[4] and self.board[1] == self.board[7]:
                return self.board[1]
        if self.board[2]:
            if self.board[2] == self.board[5] and self.board[2] == self.board[8]:
                return self.board[2]
            if self.board[2] == self.board[4] and self.board[2] == self.board[6]:
                return self.board[2]
        if self.board[3]:
            if self.board[3] == self.board[4] and self.board[3] == self.board[5]:
                return self.board[3]
        if self.board[6]:
            if self.board[6] == self.board[7] and self.board[6] == self.board[8]:
                return self.board[6]
        if 0 not in self.board:
            return -1  # stalemate
        return 0

    def submitTurn(self, uid, move):
        move = int(move)
        if uid != self.toMove() or self.board[move] or self.checkWin():
            return -1
        if self.toMove() == self.uidp1:
            self.board[move] = 1
        else:
            self.board[move] = 2
        if self.checkWin():
            self.agent.updatePolicy()
            return 0
        if self.toMove() == AIUID:
            self.submitTurn(AIUID, self.agent.nextMove())
        else:
            self.submitTurn("TRAINER", random.choice([i for i, x in enumerate(self.board) if x == 0]))
        return 0


### Machine Learning ###
class Agent:
    def __init__(self, game):
        self.symmetries = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [6, 3, 0, 7, 4, 1, 8, 5, 2],
            [8, 7, 6, 5, 4, 3, 2, 1, 0],
            [2, 5, 8, 1, 4, 7, 0, 3, 6]
        ]
        self.game = game
        self.policy = {}
        cur = db.cursor()
        cur.execute("SELECT * FROM policy")
        rows = cur.fetchall()
        for row in rows:
            self.policy[row[0]] = {
                'values': [
                    row[1], row[2], row[3], 
                    row[4], row[5], row[6], 
                    row[7], row[8], row[9]
                ],
                'counts': [
                    row[10], row[11], row[12], 
                    row[13], row[14], row[15], 
                    row[16], row[17], row[18]
                ]
            }
        self.episode = []

    def nextMove(self):
        inputstate = self.game.boardState()
        s = f"{inputstate:09d}"
        orients = [int(s)]
        for orientation in self.symmetries[1:]:
            sid = ''
            for position in orientation:
                sid += s[position]
            orients.append(int(sid))
        sid = min(orients)
        orientation = orients.index(sid)
        options = [i for i, x in enumerate(self.game.board) if x == 0]
        move = options[0]
        if random.random() < EPSILON or sid not in self.policy:
            move = random.choice(options)
        else:
            pvals = []
            for i in range(len(self.game.board)):
                j = self.symmetries[orientation].index(i)
                if i not in options:
                    pvals.append(float("-inf"))
                    continue
                pvals.append(self.policy[sid]['values'][j])
            move = random.choice([i for i, x in enumerate(pvals) if x == max(pvals)])
        self.episode.append((sid, self.symmetries[orientation].index(move)))
        return move

    def updatePolicy(self):
        result = self.game.checkWin()
        reward = 0.0
        if result == 1:
            reward = 1.0
        elif result == 2:
            reward = -1.0
        cur = db.cursor()
        for turn in reversed(self.episode):
            vf = "value" + str(turn[1])
            cf = "count" + str(turn[1])
            query = "INSERT OR IGNORE INTO policy (id) VALUES (?)"
            cur.execute(query, (turn[0],))
            value = reward
            if turn[0] in self.policy:
                p = self.policy[turn[0]]
                ratio = 1.0 / max(1, p['counts'][turn[1]])
                error = reward - p['values'][turn[1]]
                value = ratio * error
            query = "UPDATE policy SET "
            query += vf + " = " + vf + " + ?, "
            query += cf + " = " + cf + " + 1 "
            query += "WHERE id = ?"
            cur.execute(query, (value, turn[0]))
        db.commit()

m = Match()
mid = m.newMatch()
m.newBoard(mid)
matches[mid] = m
for _ in range(1000):
    m.newBoard(mid)
