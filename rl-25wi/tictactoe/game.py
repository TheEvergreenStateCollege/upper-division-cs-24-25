from flask import Flask, render_template, url_for, make_response, request, jsonify, g
import random
import string
import secrets
import json
import sqlite3

app = Flask(__name__)


class Match:
    def __init__(self, uidp1):
        self.uidp1 = uidp1
        self.uidp2 = ""
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.toMove = uidp1

    def currentTurn(self):
        return 10 - self.board.count(0)

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
        return 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


matches = {}
yearsec = 31536000

DATABASE = "./database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def newMatchID():
    characters = string.ascii_letters + string.digits
    while True:
        id = "".join(random.choice(characters) for _ in range(5))
        if id in matches:
            continue
        else:
            return id


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
    matchID = newMatchID()
    uid = request.cookies.get("uid")
    resp = make_response()
    if not uid:
        uid = secrets.token_hex(32)
        resp.set_cookie("uid", uid, max_age=yearsec)
    matches[matchID] = Match(uid)
    # Store the new match into the database with player 2 empty
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO matches (player1, player2, matchID) VALUES (?, ?, ?)",
        (uid, "", matchID),
    )
    cur.execute(
        "INSERT INTO boards (index0, index1, index2, index3, index4, index5, index6, index7, index8, match) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (0, 0, 0, 0, 0, 0, 0, 0, 0, cur.lastrowid),
    )
    db.commit()
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
        resp.set_cookie("uid", uid, max_age=yearsec)
        m.addPlayer(uid)
    else:
        uid = ""
        resp.set_cookie("uid", uid, max_age=yearsec)
    if uid != m.uidp1 and m.uidp2 == "":
        if m.addPlayer(uid) != 0:
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
        r = Match(uid)
        if uid == m.uidp1:
            r.addPlayer(m.uidp2)
        else:
            r.addPlayer(m.uidp1)
        matches[game] = r
    resp = make_response()
    if request.is_json:
        resp.headers["Content-Type"] = "application/json"
        resp.set_data('{"result": "success"}')
        return resp, 200
    resp.headers["location"] = url_for("show_board", game=game)
    return resp, 302


if __name__ == "__main__":
    app.run(debug=True)
