from flask import Flask, render_template
import json
app = Flask(__name__)
#import Map

@app.route('/')
def index():
    return render_template("Main.html", games = [[0,1], [1,2], [2,0]])

@app.route('/game/<int:game_num>')
def join_game(game_num):
    '''
    Join game number <game_num> given in the URL
    '''
    #m = Map.Map("type1")
    return render_template("Game.html")

@app.route('/update_instructions', methods=["GET", "POST"])
def get_instructions():
    '''
    Updates the instructions for a given picobot
    '''
    return json.dumps("hello")