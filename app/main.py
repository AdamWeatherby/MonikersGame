from flask import Flask
from flask import render_template
from flask import request

import requests
import random

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template("index.html")

@app.route('/start')
def start():
	print(request.args)
	numberOfPlayers = request.args.get('p', default = 2, type = int)
	print(numberOfPlayers)

	numberOfCards = 10 * numberOfPlayers

	cardsDict = []

	S = requests.Session()

	URL = "https://en.wikipedia.org/w/api.php"

	PARAMS = {
		"action": "query",
		"format": "json", 
		"list": "mostviewed", 
		"pvimlimit": "500"
	}

	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()

	MOSTVIEWED = DATA["query"]["mostviewed"]

	for i in range(0, numberOfCards):
		index = random.randint(2, 499)
		cardsDict.append(MOSTVIEWED[index]["title"])
		print(MOSTVIEWED[index]["title"])

	return "Start game with " + str(numberOfPlayers) + " players"