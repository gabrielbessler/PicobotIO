from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Main.html", games = [[0,1], [1,2], [2,0]])

@app.route('/game/<int:game_num>')
def join_game(game_num):
    '''
    Join game number <game_num> given in the URL
    '''
    return render_template("Game.html")