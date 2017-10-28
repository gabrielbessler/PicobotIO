from flask import Flask, render_template, request, abort
import json
import Map
from Game import Game
from Picobot import Picobot
from threading import Timer
app = Flask(__name__)

games = [[0,0], [1,0], [2,0]]
game_boards = {}
game_timers = {}
GAME_TIME = 5

@app.route('/')
def index():
    '''
    '''
    return render_template("Main.html", games = games)

@app.route('/game/<int:game_num>')
def join_game(game_num):
    '''
    Join game number <game_num> given in the URL
    '''
    if game_num >= len(games):
        abort(404)
    games[game_num][1] += 1
    if games[game_num][1] == 2:

        #First, we create a map
        m = Map.Map("type1")
        g = Game(m)

        game_boards[game_num] = g
        game_timers[0] = 5
        Timer(1, update_data, [5, game_num]).start()
        return render_template("Game.html", score=[0,GAME_TIME,0])
    else:
        return "loading..."

@app.route('/get_score', methods=["POST"])
def get_score():
    if game_boards[0] == -1:
        return json.dumps(-1)
    score = game_boards[0].getScore()
    return json.dumps([score[1],game_timers[0],score[0]])


def update_data(counter, game_num):
    '''
    '''
    game_timers[0] = counter
    if counter == 0:
        Timer(1, update_game, [GAME_TIME, game_num]).start()
    else:
        Timer(1, update_data, [counter - 1, game_num]).start()

def update_game(counter, game_num):
    '''
    '''
    if counter == 0:
        game_boards[game_num] = -1
        games[game_num][1] = 0
    else:
        game_timers[0] = counter
        game_boards[game_num].update()
        Timer(.5, update_game, [counter - .5, game_num]).start()

@app.route('/get_map', methods=["POST"])
def get_map():
    '''
    '''
    if game_boards[0] == -1:
        return "poop"
    return json.dumps(game_boards[0].map.getMap())

@app.route('/update_instructions', methods=["GET", "POST"])
def get_instructions():
    '''
    Updates the instructions for a given picobot
    '''
    L = request.get_json()
    ruleList = []
    for i in L:
        i.replace(" ", "")
        if(i[0] != '[' or i[11] != ']'):
            return json.dumps("Start and end with square brackets.")
        elif not (RepresentsInt(i[1]) and RepresentsInt(i[10])):
            return json.dumps("Current and next states must be ints.")
        else:
            directions = i[3:7] + [i[8]]
            if not (isDirections(directions)):
                return json.dumps("Use valid direction operators.")
	ruleList.append([int(i[1]), i[3:7], i[8], int(i[10]))
        game_boards[0].bot1.rules = ruleList
    return json.dumps("Your inputs are valid.")

def isDirections(s):
    if not(s[0] == "_" or s[0] == "*" or s[0] == "x"):
        return False
    elif not(s[1] == "_" or s[1] == "*" or s[1] == "x"):
        return False
    elif not(s[2] == "_" or s[2] == "*" or s[2] == "x"):
        return False
    elif not(s[3] == "_" or s[3] == "*" or s[3] == "x"):
        return False
    elif not(s[4] == "_" or s[4] == "_" or s[4] == "_" or s[4] == "_"):
        return False
    else:
        return True

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@app.route('/create_game', methods=["POST"])
def create_new_game():
    '''
    Adds a new game to the games list
    '''
    games.append([len(games),0])
    return json.dumps("Success")

@app.errorhandler(404)
def page_not_found(e):
    '''
    '''
    return render_template('404.html')
