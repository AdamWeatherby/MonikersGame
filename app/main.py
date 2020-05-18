from flask import Flask
from flask import render_template
from flask import request

import requests
import random
import json

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

	cardsTitles = []

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
		cardsTitles.append(MOSTVIEWED[index]["title"])
		print(MOSTVIEWED[index]["title"])


	cardsDict = {}
	for title in cardsTitles:
		PARAMS = {
			"action": "query",
			"format": "json",
			"prop": "extracts",
			"titles": title,
			"exsentences": "5",
			"exlimit": "1",
			"explaintext": "1",
			"formatversion": "2"
		}
		R = S.get(url=URL, params=PARAMS)
		DATA = R.json()

		description = DATA["query"]["pages"][0]["extract"]
		cardsDict[title] = description
	return "Start game with " + str(numberOfPlayers) + " players"