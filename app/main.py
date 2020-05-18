from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template("index.html")

@app.route('/start')
def start():
	print(request.args)
	numberOfPlayers = request.args.get('p', default = 2, type = int)
	print(numberOfPlayers)
	return "Start game with " + str(numberOfPlayers) + " players"