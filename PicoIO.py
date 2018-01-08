from flask import Flask, render_template, request, abort, session, url_for
from threading import Timer
from random import randint
from Game import Game
import datetime
import logging
import pymongo
import json
import Map
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)  # used for user sessions

# Constants related to the game
STARTUP_TIME = 10
GAME_TIME = 5
ITEM_DELAY = 10
MAX_ITEMS = 10
MAX_GAMES = 100

# Stores all of the game information
games = [0, 0, 0]
game_players = {}
game_boards = {}
game_timers = {}
NUM_ID = [0]

# ================ Mongo Handler =============


class MongoHandler:

    def __init__(self):
        '''
        Connects to the MongoDB file
        '''
        self.client = pymongo.MongoClient()
        self.db = self.client.PicoIOData
        self.collection = self.db.PicoData

    def is_user(self, username):
        '''
        Given a username as a string,
        returns true a user exists with that username
        '''
        user = self.collection.find_one({"username": username})
        if user is None:
            return False
        return True

    def insert_new_user(self, username, password):
        '''
        Given a username and password as strings,
        creates a new user in the database if a user with the
        given username does not already exist
        '''
        if not self.is_user(username):
            document = {
                "username": username,
                "password": password,
                "wins": 0,
                "losses": 0,
                "registry_date": datetime.datetime.utcnow()}
            self.collection.insert_one(document)
        else:
            return ValueError("Username already in use.")

    def login(self, username, password):
        '''
        Given a username and a password as strings,
        sees if the given password is correct for the given
        username
        '''
        if True:
            return True
        else:
            raise ValueError("Incorrect password")

    def reset_password(self, username, password):
        '''
        Changes the password for a given username
        '''
        pass

    def get_profile_info(self, username):
        '''
        Given a username, returns a list with the user info in the form
        [name, wins, losses, win/loss ratio, title]
        '''
        if not self.is_user(username):
            raise ValueError("Not a valid username")
        else:
            user_info = self.collection.find_one({"username": username})
            title = ""
            wins = user_info['wins']
            losses = user_info['losses']

            # TODO: use this instead and add a get_title() method that works
            # efficiently
            title_requirements = {"Rookie": 1, "Soldier": 5,
                                  "Battlemaster": 25, "Destroyer": 100}

            if wins >= 1:
                title = "Rookie"
            elif wins >= 5:
                title = "Soldier"
            elif wins >= 25:
                title = "Battlemaster"
            elif wins >= 100:
                title = "Destroyer"

            if losses == 0:
                if wins == 0:
                    winloss = 50
                else:
                    winloss = wins*100
            else:
                winloss = round(100*(wins/losses))

            profile_info = [username, wins, losses,
                            winloss, title]

            return profile_info


# ================ INDEX =====================


@app.route('/')
def index():
    '''
    Main lobby/waiting screen
    '''
    return render_template("index.html",
                           list_of_games=games)


@app.route('/get_game_list', methods=["POST"])
def get_game_list():
    '''
    Returns the list of games currently available
    '''
    return json.dumps(games)


@app.route('/quick_join/', methods=["POST"])
def quick_join():
    for game in games:
        if game < 2:
                return json.dumps('/game/' + str(game))
    return json.dumps("error")

# ================ MAIN GAME =================


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
                    if games[game_num] == 1:
                        return render_template("waiting.html")
                    else:
                        if session["player_ID"] == game_players[game_num][0]:
                            return render_template("game.html",
                                                   score=[0, GAME_TIME, 0],
                                                   player_num=1,
                                                   game_num=game_num)
                        else:
                            return render_template("game.html",
                                                   score=[0, GAME_TIME, 0],
                                                   player_num=2,
                                                   game_num=game_num)
                else:
                    err = "Game Full..."
                    return render_template('error_disp.html', error_code=err)
            except:
                # If the game is empty, this means that the player was/is part
                # of ANOTHER game, but not this one
                err = "You are already in another queue or match."
                return render_template('error_disp-disp.html', error_code=err)

        else:
            # first, we check how many players are in the game
            if games[game_num] < 2:
                # if it's less than 2, we want to add a new player
                if games[game_num] == 0:
                    game_players[game_num] = [NUM_ID[0]]
                    games[game_num] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("waiting.html", game_num=game_num)
                else:
                    game_players[game_num].append(NUM_ID[0])
                    m = Map.Map("islands")
                    g = Game(m, ITEM_DELAY)
                    game_boards[game_num] = g
                    game_timers[game_num] = STARTUP_TIME
                    Timer(1, update_data, [STARTUP_TIME, game_num]).start()
                    games[game_num] += 1
                    session["player_ID"] = NUM_ID[0]
                    NUM_ID[0] += 1
                    return render_template("game.html",
                                           score=[0, GAME_TIME, 0],
                                           player_num=2,
                                           game_num=game_num)
            else:
                s = "Game full..."
                return render_template('error_disp.html', error_code=s)


@app.route('/check_game_ready/<int:game_num>', methods=["POST"])
def check_game_ready(game_num):
    if game_num not in game_players:
        return json.dumps(1)
    # TODO: consider using defaultdict
    if len(game_players[game_num]) == 2:
        return json.dumps(url_for('join_game', game_num=game_num)[1:])
    else:
        return json.dumps(1)


@app.route("/login", methods=["POST"])
def login():
    '''
    Attempts to login to an account in the database
    '''
    try:
        data = request.get_json()
        mongo_handler.login(data['username'], data['password'])
        return "successful login"
    except ValueError as error:
        return error.args


@app.route("/register", methods=["POST"])
def register():
    '''
    Registers a new user in the database
    '''
    try:
        data = request.get_json()
        mongo_handler.insert_new_user(data['username'], data['password'])
        return "Success"
    except ValueError as error:
        return error.args


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
        games[game_num] = 0
        game_players[game_num] = []
    else:
        if game_boards[game_num].curr_num_items < MAX_ITEMS:
            game_boards[game_num].spawn_item()

        game_timers[game_num] = counter
        game_boards[game_num].update()
        Timer(.25, update_game, [counter - .25, game_num]).start()


@app.route('/update_instructions/<int:game_num>', methods=["POST"])
def get_instructions(game_num):
    '''
    Updates the instructions for a given picobot
    '''
    L = request.get_json()
    playerNum = int(L[0])
    L = eval("[" + L[1:] + "]")
    ruleList = []
    for i in L:
        i = str(i).replace(" ", "")
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
    for index in range(4):
        if not(s[index] == "_" or s[index] == "*" or s[index] == "x"):
            return False
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
    global games
    if len(games) < MAX_GAMES:
        games += [0]
        return json.dumps("Success")
    return json.dumps("Failure")


@app.route('/get_profile/<string:profile_name>', methods=["POST"])
def get_profile(profile_name):
    '''
    Returns the HTML representation of the profile_info
    to be display for the user's OWN profile
    '''
    L = mongo_handler.get_profile_info(profile_name)

    return render_template("profile_info.html", name=L[0],
                           wins=L[1], losses=L[2],
                           winloss=L[3], title=L[4])


@app.errorhandler(404)
def page_not_found(e):
    '''
    Displays a "page not found" error for 404 errors
    '''
    err = "Oops, you've taken a wrong turn."
    return render_template('error_disp.html', error_code=err)


@app.errorhandler(405)
def method_not_alloed(e):
    return page_not_found(e)


@app.route('/profile/<string:profile_name>')
def profile(profile_name):
    # name, wins, losses, winloss, title
    try:
        L = mongo_handler.get_profile_info(profile_name)

        return render_template("profile.html", name=L[0], wins=L[1],
                               losses=L[2], winloss=L[3], title=L[4])
    except ValueError as err:
        err_msg = "The user " + profile_name + " does not exist"
        return render_template("error_disp.html", error_code=err_msg)


@app.route('/exit_game/<int:game_num>', methods=["POST"])
def exit_game(game_num):
    # the only case when this can happen is if there is only one person in
    #  queue
    # (if there are two, then the game has already started and you cannot
    # leave )
    if games[game_num] == 1:
        games[game_num] = 0
        game_players[game_num] = []
        return 'true'
    return 'err'


if __name__ == "__main__":
    mongo_handler = MongoHandler()
    app.run(host='0.0.0.0')
