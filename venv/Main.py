from flask import Flask, render_template, request, abort, session
from threading import Timer
from Picobot import Picobot
from random import randint
from Game import Game
from Item import Item
import json
import Map
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # used for user sessions

# Stores all of the game information
games = [[0, 0], [1, 0], [2, 0]]
STARTUP_TIME = 10
game_players = {}
game_boards = {}
game_timers = {}
GAME_TIME = 1000
NUM_ID = [0]


@app.route('/')
def index():
    '''
    Main lobby/waiting screen
    '''
    return render_template("Main.html", games=games)


@app.route('/game/<int:game_num>')
def join_game(game_num):
    '''
    Join game number <game_num> given in the URL
    '''
    if game_num >= len(games):
        abort(404)
    else:
        if "player_ID" in session:
            if session["player_ID"] == game_players[game_num][0] or \
               session["player_ID"] == game_players[game_num][1]:
                if games[game_num][1] == 1:
                    return render_template("waiting.html")
                else:
                    if session["player_ID"] == game_players[game_num][0]:
                        return render_template("Game.html",
                                               score=[0, GAME_TIME, 0],
                                               player_num=1)
                    else:
                        return render_template("Game.html",
                                               score=[0, GAME_TIME, 0],
                                               player_num=2)
            else:
                return "Game Full...<a href='/'>go home.</a>"
        else:
            # first, we check how many players are in the game
            if games[game_num][1] < 2:
                # if it's less than 2, we want to add a new player
                if games[game_num][1] == 0:
                    game_players[game_num] = [NUM_ID[0]]
                    games[game_num][1] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("waiting.html")
                else:
                    game_players[game_num].append(NUM_ID[0])
                    m = Map.Map("islands")
                    g = Game(m)
                    game_boards[game_num] = g
                    game_timers[0] = STARTUP_TIME
                    Timer(1, update_data, [STARTUP_TIME, game_num]).start()
                    games[game_num][1] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("Game.html",
                                           score=[0, GAME_TIME, 0],
                                           player_num=2)
            else:
                return "Game Full...<a href='/'>go home.</a>"


@app.route('/get_score', methods=["POST"])
def get_score():
    '''
    Calculate and return the score of each player in the game
    '''
    if len(game_boards) >= 1:
        if game_boards[0] == -1:
            return json.dumps(-1)
        score = game_boards[0].getScore()
        return json.dumps([score[1], game_timers[0], score[0],
                          game_boards[0].map.getMap()])
    return json.dumps("-2")


def update_data(counter, game_num):
    '''
    Countdown before the game actually starts
    '''
    game_timers[0] = counter
    if counter <= 0:
        print('test')
        Timer(1, update_game, [GAME_TIME, game_num]).start()
    else:
        Timer(1, update_data, [counter - 1, game_num]).start()


def update_game(counter, game_num):
    '''
    Countdown and update the game until the game ends
    '''
    if counter <= 0:
        game_boards[game_num] = -1
        games[game_num][1] = 0
    else:
        r = randint(1, 3)
        if r == 1:
            i = Item(1)
            print('creating item')
            game_boards[game_num][randint(0, 19), randint(0, 19)] = i
        game_timers[0] = counter
        game_boards[game_num].update()
        Timer(.5, update_game, [counter - .5, game_num]).start()


@app.route('/update_instructions', methods=["GET", "POST"])
def get_instructions():
    '''
    Updates the instructions for a given picobot
    '''
    L = request.get_json()
    playerNum = int(L[0])
    L = eval("[" + L[1:] + "]")
    ruleList = []
    for i in L:
        i = str(i)
        i = i.replace(" ", "")
        if(i[0] != '[' or i[15] != ']'):
            return json.dumps("Start and end with square brackets.")
        elif not (represents_int(i[1]) and represents_int(i[14])):
            return json.dumps("Current and next states must be ints.")
        else:
            directions = i[4:8] + i[11]
            if not (is_directions(directions)):
                return json.dumps("Use valid direction operators.")

            ruleList.append([int(i[1]), i[4:8], i[11], int(i[14])])
    if playerNum == 1:
        game_boards[0].bot2.ruleList = ruleList
    else:
        game_boards[0].bot1.ruleList = ruleList

    return json.dumps("Your inputs are valid.")


def is_directions(s):
    '''
    Given a string S representing the environment segment of an instruction,
    check if the environement is in the correct format
    '''
    if not(s[0] == "_" or s[0] == "*" or s[0] == "x"):
        return False
    elif not(s[1] == "_" or s[1] == "*" or s[1] == "x"):
        return False
    elif not(s[2] == "_" or s[2] == "*" or s[2] == "x"):
        return False
    elif not(s[3] == "_" or s[3] == "*" or s[3] == "x"):
        return False
    elif not(s[4] == "N" or s[4] == "S" or s[4] == "W" or s[4] == "E"):
        return False
    else:
        return True


def represents_int(s):
    '''
    Checks if a number can be represntated as an integer
    '''
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
    games.append([len(games), 0])
    return json.dumps("Success")


@app.errorhandler(404)
def page_not_found(e):
    '''
    Displays a "page not found" error for 404 errors
    '''
    return render_template('404.html')
