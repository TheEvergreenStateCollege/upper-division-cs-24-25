from flask import Flask, render_template, url_for, make_response, request, jsonify, g
import random
import string
import secrets
import json
import sqlite3


### Configuration Values ###
DATABASE = "data.db" # relative path
MAXAGE = 31536000 # for cookie, one year
EPSILON = 0.1 # Rate of random moves
AIUID = "WOPR" # WarGames reference


### Initial Setup ###
app = Flask(__name__)


### Database Functions ###
def getDB():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close() 

def load_matches():
    matches = {}
    rows = []
    with app.app_context():
        cur = getDB().cursor()
        query = "SELECT m.id, m.player1, m.player2, "
        query += "b.id, b.index0, b.index1, b.index2, "
        query += "b.index3, b.index4, b.index5, b.index6, "
        query += "b.index7, b.index8 FROM boards AS b "
        query += "JOIN matches AS m ON b.match=m.id "
        query += "ORDER BY b.created"
        cur.execute(query)
        rows = cur.fetchall()
    for row in rows:
        m = Match(row[1], row[2])
        m.boardID = row[3]
        m.board = [
            row[4], row[5], row[6],
            row[7], row[8], row[9],
            row[10], row[11], row[12]
        ]
        if m.uidp1 == AIUID or m.uidp2 == AIUID:
            m.agent = Agent(m)
        if m.agent and m.toMove() == AIUID:
            m.submitTurn(AIUID, m.agent.nextMove())
        matches[row[0]] = m
    return matches


### Game Logic ###
class Match:
    def __init__(self, uidp1, uidp2=''):
        self.uidp1 = uidp1
        self.uidp2 = uidp2
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.agent = None
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
        if self.uidp1 == AIUID or self.uidp2 == AIUID:
            self.agent = Agent(self)
        characters = string.ascii_letters + string.digits
        matchID = "".join(random.choice(characters) for _ in range(5))
        while matchID in matches:
            matchID = "".join(random.choice(characters) for _ in range(5))
        with app.app_context():
            db = getDB()
            cur = db.cursor()
            query = "INSERT INTO matches (id, player1, player2) VALUES (?, ?, ?)"
            cur.execute(query, (matchID, self.uidp1, self.uidp2))
            db.commit()
        return matchID

    def newBoard(self, matchID):
        with app.app_context():
            db = getDB()
            cur = db.cursor()
            cur.execute("INSERT INTO boards (match) VALUES (?)", (matchID,))
            self.boardID = cur.lastrowid
            db.commit()
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if self.agent:
            self.agent = Agent(self)
            if self.toMove() == AIUID:
                self.submitTurn(AIUID, self.agent.nextMove())

    def addPlayer(self, uidp2):
        if self.uidp2 == "":
            self.uidp2 = uidp2
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
        if uid != self.toMove() or self.board[move] or self.checkWin():
            return -1
        if self.uidp1 == self.uidp2:
            if self.board.count(1) > self.board.count(2):
                self.board[move] = 2
            else:
                self.board[move] = 1
        else:
            if self.toMove() == self.uidp1:
                self.board[move] = 1
            else:
                self.board[move] = 2
        with app.app_context():
            db = getDB()
            cur = db.cursor()
            query = "UPDATE boards SET "
            query += "index" + str(move) + " = ? "
            query += "WHERE id = ?"
            cur.execute(query, (self.board[move], self.boardID))
            db.commit()
        if self.agent:
            if self.checkWin():
                self.agent.updatePolicy()
                return 0
            if self.toMove() == AIUID:
                self.submitTurn(AIUID, self.agent.nextMove())
        return 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


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
        rows = []
        with app.app_context():
            cur = getDB().cursor()
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
        with app.app_context():
            db = getDB()
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
        resp.set_cookie("uid", value=uid, max_age=MAXAGE)
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

@app.route("/new_bot_game")
def new_bot_game():
    uid = request.cookies.get("uid")
    resp = make_response()
    if not uid:
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", value=uid, max_age=MAXAGE)
    m = Match(AIUID, uid)
    matchID = m.newMatch()
    m.newBoard(matchID)
    matches[matchID] = m
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"gameid": "' + matchID + '"}')
        return resp, 200
    resp.headers["location"] = url_for("show_board", game=matchID)
    return resp, 302

@app.route("/new_share_game")
def new_share_game():
    uid = request.cookies.get("uid")
    resp = make_response()
    if not uid:
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", value=uid, max_age=MAXAGE)
    m = Match(uid, uid)
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
    if m.uidp1 == m.toMove():
        tomove = 1
    if win:
        tomove = 0
    if m.uidp1 == m.uidp2:
        if m.board.count(1) > m.board.count(2):
            side = 2
            tomove = 2
        else:
            side = 1
            tomove = 1
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
    if uid is None:
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", value=uid, max_age=MAXAGE)
        m.addPlayer(uid)
    else:
        resp.set_cookie("uid", value=uid, max_age=MAXAGE)
    if uid != m.uidp1 and m.uidp2 == "":
        if m.addPlayer(uid):
            return "Already two players", 403
    result = m.submitTurn(uid, move)
    if result < 0:
        result = "invalid move"
    else:
        result = "success"
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"result": "' + result + '"}')
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


### Run App ###
matches = load_matches()
if __name__ == "__main__":
    app.run(debug=True)
