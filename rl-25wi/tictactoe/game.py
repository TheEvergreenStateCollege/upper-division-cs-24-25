from flask import Flask, render_template, redirect, url_for
import random
import string

app = Flask(__name__)
app.secret_key = ""


class Match:
    def __init__(self, uidp1):
        self.uidp1 = uidp1
        self.uidp2 = ""
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.toMove = uidp1

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
        if uid != self.toMove or self.board[move]:
            return -1
        if self.toMove == self.uidp1:
            self.board[move] = 1
            self.toMove = self.uidp2
        else:
            self.board[move] = 2
            self.toMove = self.uidp1
        return 0


matches = {}


def newMatchID():
    characters = string.ascii_letters + string.digits
    while ():
        id = "".join(random.choice(characters) for _ in range(5))
        if id in matches:
            continue
        else:
            return id


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/new_game")
def new_game():
    matchID = newMatchID()
    player1 = 0
    matches[matchID] = Match(player1)
    return redirect(url_for("show_board", game=matchID))


@app.route("/<game>")
def show_board():
    return render_template("board.html")


@app.route("/<game>/<move>")
def make_move(game, move):
    player = 0
    match = matches[game]
    if player != match.uidp1:
        if match.addPlayer(player):
            return "Already two players", 403
    result = match.submitTurn(player, move)
    if result < 0:
        return "Invalid Move", 403
    return redirect(url_for("show_board", game=game))
