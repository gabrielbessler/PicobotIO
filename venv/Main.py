from flask import Flask, render_template, request
import json
import Map
app = Flask(__name__)

games = [[0,0], [1,0], [2,0]]

@app.route('/')
def index():
    return render_template("Main.html", games = [[0,1], [1,2], [2,0]])

@app.route('/game/<int:game_num>')
def join_game(game_num):
    '''
    Join game number <game_num> given in the URL
    '''
    games[game_num][1] += 1
    if games[game_num][1] == 2:
        m = Map.Map("type1")
        return render_template("Game.html")

@app.route('/update_instructions', methods=["GET", "POST"])
def get_instructions():
    '''
    Updates the instructions for a given picobot
    '''
    L = request.get_json()
    for i in L:
        print(i)
    return json.dumps("hello")

@app.route('/create_game', methods=["POST"])
def create_new_game():
    '''
    Adds a new game to the games list
    '''
    games.append([len(games),0])
    return json.dumps("Success")