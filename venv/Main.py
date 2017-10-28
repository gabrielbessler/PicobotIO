from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("Main.html", game = [[0,1], [1,2], [2,0]])