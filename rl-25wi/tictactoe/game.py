from flask import Flask, render_template, url_for, make_response, request, jsonify
import random
import string
import secrets
import json
import sqlite3


### Configuration Values ###
DATABASE = "data.db" # relative path
MAXAGE = 31536000 # for cookie, one year
EPSILON = 0.1 # Rate of random moves
GAMMA = 0.9 # Discount over distance from reward
AIUID = "WOPR" # WarGames reference


### Initial Setup ###
app = Flask(__name__)
db = sqlite3.connect(DATABASE)
# Collect matches from DB
matches = {}
cur = db.cursor()
query = "SELECT m.id, m.player1, m.player2, "
query += "b.id, b.index0, b.index1, b.index2, "
query += "b.index3, b.index4, b.index5, b.index6, "
query += "b.index7, b.index8, FROM boards AS b "
query += "JOIN matches AS m ON b.match=m.id "
query += "ORDER BY b.created"
cur.execute(query)
rows = cur.fetchall()
for row in rows:
    m = Match(row[2])
    m.boardID = row[3]
    m.uidp1 = row[1]
    m.board = [
        row[4], row[5], row[6],
        row[7], row[8], row[9],
        row[10], row[11], row[12]
    ]
    matches[row[0]] = m

@app.teardown_appcontext
def close_db(exception):
    if db is not None:
        db.close()


### Game Logic ###
class Match:
    def __init__(self, uidp2):
        self.uidp1 = AIUID
        self.uidp2 = uidp2
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.toMove = self.uidp1
        self.agent = Agent(self)
        
    def currentTurn(self):
        return 10 - self.board.count(0)

    def boardState(self):
        return int(''.join(str(num) for num in self.board))

    def newMatch():
        characters = string.ascii_letters + string.digits
        matchID = "".join(random.choice(characters) for _ in range(5))
        while matchID in matches:
            matchID = "".join(random.choice(characters) for _ in range(5))
        cur = db.cursor()
        query = "INSERT INTO matches (id, player1, player2) VALUES (?, ?, ?)"
        cur.execute(query, (matchID, self.uidp1, self.uidp2))
        db.commit()
        return matchID

    def newBoard(matchID):
        cur = db.cursor()
        cur.execute("INSERT INTO boards (match) VALUES (?)", matchID)
        self.boardID = cur.lastrowid
        db.commit()
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.toMove = self.uidp1
        if self.toMove == AIUID:
            self.submitTurn(AIUID, self.agent.nextMove())

    def addPlayer(self, uidp2):
        if self.uidp2 == "":
            self.uidp2 = uidp2
            if self.toMove != self.uidp1:
                self.toMove = self.uidp2
            return 0  # Added player 2
        else:
            return -1  # Already a player 2

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
        if uid != self.toMove or self.board[move] or self.checkWin():
            return -1
        if self.toMove == self.uidp1:
            self.board[move] = 1
            self.toMove = self.uidp2
        else:
            self.board[move] = 2
            self.toMove = self.uidp1
        cur = db.cursor()
        query = "UPDATE boards SET "
        query += "index" + str(move) + " = ? "
        query += "WHERE id = ?"
        cur.exec(query, (self.board[move], self.boardID))
        db.commit()
        if self.toMove = AIUID:
            if self.checkWin():
                self.agent.updatePolicy()
            else:
                self.submitTurn(AIUID, self.agent.nextMove())
        return 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


### Machine Learning ###
class Agent:
    def __init__(self, game):
        self.symmetries = [
            [6, 3, 0, 7, 4, 1, 8, 5, 2],
            [8, 7, 6, 5, 4, 3, 2, 1, 0],
            [2, 5, 8, 1, 5, 7, 0, 3, 6]
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
        for orientation in self.symmetries:
            sid = ''
            for position in orientation:
                sid += s[position]
            orients.append(int(sid))
        sid = min(orients)
        orientation = orients.index(sid)
        options = [i for i, x in enumerate(self.game.board) if x == 0]
        move = options[0]
        if random.random() < EPSILON:
            move = random.choice(options)
        else:
            pvals = self.policy[sid].values
            move = max(range(len(pvals)), key=pvals.__getitem__)
        self.episode.append((sid, move))
        if orientation > 0:
            move = self.symmetries[orientation-1][move]
        return move

    def updatePolicy(self):
        result = game.checkWin()
        reward = 0
        if result == 1:
            reward = 1
        elif result == 2:
            reward = -1
        # scale = GAMMA
        cur = db.cursor()
        for turn in reversed(self.episode):
            p = self.policy[turn[0]]
            ratio = 1 / p.counts[turn[1]]
            error = reward - p.values[turn[1]]
            # value = scale * ratio * error
            value = ratio * error
            vf = "val" + str(turn[1])
            cf = "count" + str(turn[1])
            query = "UPDATE policy SET "
            query += vf + " = " + vf + " + ?, "
            query += cf + " = " + cf + " + 1 "
            query += "WHERE id = ?"
            cur.exec(query, (value, turn[0]))
            # scale *= GAMMA
        db.commit()


### Routes ###
@app.route("/")
def home():
    if request.is_json:
        return (
            '{"message": "Welcome! Go to /new_game to create a new game, and go to /<gameid> to join one."}',
            200,
        )
    return render_template("home.html")

@app.route("/new_game")
def new_game():
    uid = request.cookies.get("uid")
    resp = make_response()
    if not uid:
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", uid, max_age=MAXAGE)
    m = Match(uid)
    matchID = m.newMatch()
    m.newBoard(matchID)
    matches[matchID] = m
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"gameid": "' + matchID + '"}')
        return resp, 200
    resp.headers["location"] = url_for("show_board", game=matchID)
    return resp, 302

@app.route("/<game>")
def show_board(game):
    if game not in matches:
        return "Game not found.", 404
    m = matches[game]
    if request.is_json:
        return jsonify(m.board), 200
    side = 0
    if request.cookies.get("uid") == m.uidp1:
        side = 1
    elif request.cookies.get("uid") == m.uidp2 or m.uidp2 == "":
        side = 2
    win = m.checkWin()
    tomove = 2
    if m.uidp1 == m.toMove:
        tomove = 1
    if win:
        tomove = 0
    return render_template(
        "board.html",
        match=m.board,
        win=win,
        turn=m.currentTurn(),
        side=side,
        tomove=tomove,
        gameid=game,
    )

@app.route("/<game>/<move>")
def make_move(game, move):
    uid = request.cookies.get("uid")
    resp = make_response()
    m = matches[game]
    if uid == "":
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", uid, max_age=MAXAGE)
        m.addPlayer(uid)
    else:
        resp.set_cookie("uid", uid, max_age=MAXAGE)
    if uid != m.uidp1 and m.uidp2 == "":
        if m.addPlayer(uid):
            return "Already two players", 403
    result = m.submitTurn(uid, move)
    if result < 0:
        return "Invalid Move", 403
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"result": "success"}')
        return resp, 200
    resp.headers["location"] = url_for("show_board", game=game)
    return resp, 302

@app.route("/<game>/rematch")
def rematch(game):
    m = matches[game]
    uid = request.cookies.get("uid")
    if uid != m.uidp1 and uid != m.uidp2:
        return "Not a Player", 403
    if m.checkWin():
        m.newBoard(game)
    resp = make_response()
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"result": "success"}')
        return resp, 200
    resp.headers["location"] = url_for("show_board", game=game)
    return resp, 302

if __name__ == "__main__":
    app.run(debug=True)
