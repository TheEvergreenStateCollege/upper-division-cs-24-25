from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/new_game")
def new_game():

@app.route("/<game>")
def show_board():
    return render_template('board.html')

@app.route("/<game>/<move>")
def make_move():
