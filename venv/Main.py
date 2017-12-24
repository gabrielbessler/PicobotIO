from flask import Flask, render_template, request, abort, session, url_for
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
ITEM_DELAY = 10
MAX_ITEMS = 10
NUM_ID = [0]
MAX_GAMES = 100
curr_num_items = [0, 0, 0]

# TEMP #
# @app.route('/jake', methods=["GET", "POST"])
# def get_jake_data():
#     return json.dumps("sample data")


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
    # If the player is trying to join a game that is not in the allowed
    # game list, exit
    if game_num >= len(games):
        abort(404)
    else:
        # otherwise, the player is trying to join a game that is allowed
        if "player_ID" in session:
            # the player already has a player_ID
            # We have to check if the game is actually a valid game
            try:
                if session["player_ID"] == game_players[game_num][0] or \
                   session["player_ID"] == game_players[game_num][1]:
                    # if the player_ID is equal to one of the two IDs in this
                    # game, let the player join the game
                    if games[game_num][1] == 1:
                        return render_template("waiting.html")
                    else:
                        if session["player_ID"] == game_players[game_num][0]:
                            return render_template("Game.html",
                                                   score=[0, GAME_TIME, 0],
                                                   player_num=1,
                                                   game_num=game_num)
                        else:
                            return render_template("Game.html",
                                                   score=[0, GAME_TIME, 0],
                                                   player_num=2,
                                                   game_num=game_num)
                else:
                    return "Game Full...<a href='/'>go home.</a>"
            except:
                # If the game is empty, this means that the player was/is part
                # of ANOTHER game, but not this one
                # TODO: what is the best way to deal with this case?
                return "Error - You are in another game!"

        else:
            # first, we check how many players are in the game
            if games[game_num][1] < 2:
                # if it's less than 2, we want to add a new player
                if games[game_num][1] == 0:
                    game_players[game_num] = [NUM_ID[0]]
                    games[game_num][1] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("waiting.html", game_num=game_num)
                else:
                    game_players[game_num].append(NUM_ID[0])
                    m = Map.Map("islands")
                    g = Game(m)
                    game_boards[game_num] = g
                    game_timers[game_num] = STARTUP_TIME
                    Timer(1, update_data, [STARTUP_TIME, game_num]).start()
                    games[game_num][1] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("Game.html",
                                           score=[0, GAME_TIME, 0],
                                           player_num=2)
            else:
                return "Game Full...<a href='/'>go home.</a>"


@app.route('/check_game_ready/<int:game_num>', methods=["POST"])
def check_game_ready(game_num):
    if game_num not in game_players:
        return json.dumps(1)
    # TODO: consider using defaultdict
    if len(game_players[game_num]) == 2:
        return json.dumps(url_for('join_game', game_num=game_num)[1:])
    else:
        return json.dumps(1)


@app.route('/get_score/<int:game_num>', methods=["POST"])
def get_score(game_num):
    '''
    Calculate and return the score of each player in the game
    '''
    # Check if the user passed in a value
    if len(game_boards) >= 1:
        try:
            if game_boards[game_num] == -1:
                # Return -1 if the game is over, and let client figure out
                # winner based on score
                return json.dumps(-1)
            score = game_boards[game_num].getScore()
            L = [score[1], game_timers[game_num], score[0],
                 game_boards[game_num].map.getMap()]
            return json.dumps(L)
        except:
            pass
    # If we cannot access the score, return -2
    # (the client will handle this as 'don't update' )
    return json.dumps(-2)


def update_data(counter, game_num):
    '''
    Countdown before the game actually starts
    '''
    game_timers[game_num] = counter
    if counter <= 0:
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
        if curr_num_items[game_num] < MAX_ITEMS:
            r = randint(1, ITEM_DELAY)
            if r == 1:
                i = Item(1)
                x_spawn = randint(0, 19)
                y_spawn = randint(0, 19)
                obj = game_boards[game_num].map.map[x_spawn][y_spawn][1]
                if obj != "Wall()":
                    curr_num_items[game_num] += 1
                    L = [game_boards[game_num].map.map[x_spawn][y_spawn][0], i]
                    game_boards[game_num].map.map[x_spawn][y_spawn] = L

        game_timers[game_num] = counter
        game_boards[game_num].update()
        Timer(.5, update_game, [counter - .5, game_num]).start()


@app.route('/update_instructions/<int:game_num>', methods=["GET", "POST"])
def get_instructions(game_num):
    '''
    Updates the instructions for a given picobot
    '''
    L = request.get_json()
    playerNum = int(L[0])
    print(playerNum)
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
        game_boards[game_num].bot2.ruleList = ruleList
    else:
        game_boards[game_num].bot1.ruleList = ruleList

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
    if len(games) < MAX_GAMES:
        games.append([len(games), 0])
        curr_num_items.append(0)
        return json.dumps("Success")
    else:
        return json.dumps("Failure")


@app.errorhandler(404)
def page_not_found(e):
    '''
    Displays a "page not found" error for 404 errors
    '''
    return render_template('404.html')


@app.errorhandler(405)
def method_not_alloed(e):
    return page_not_found(e)


@app.route('/profile/<string:profile_name>')
def profile(profile_name):
    return render_template("profile.html")


@app.route('/exit_game/<int:game_num>')
def exit_game(game_num):
    # TODO
    print("removing player from game...")


@app.route('/quick_join/', methods=["POST"])
def quick_join():
    for game in games:
        if game[1] < 2:
                return json.dumps('/game/' + str(game[0]))

    return json.dumps("error")
