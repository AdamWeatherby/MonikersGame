from flask import Flask
from flask import render_template
from flask import request

import requests
import random
import json

app = Flask(__name__)

class Card:
	def __init__(self, title, description, value):
		self.title = title
		self.description = description
		self.value = value

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
		title = MOSTVIEWED[index]["title"]
		if(not("list" in title or "user" in title)):

			if(index < 125):
				score = 1
			elif(index < 250):
				score = 2
			elif(index < 375):
				score = 3
			else:
				score = 4



			card = Card(title, "", score)
			cardsTitles.append(card)
			print(title)
		else:
			i = i-1


	cards = []
	for card in cardsTitles:
		PARAMS = {
			"action": "query",
			"format": "json",
			"prop": "extracts",
			"titles": card.title,
			"exsentences": "5",
			"exlimit": "1",
			"explaintext": "1",
			"formatversion": "2"
		}
		R = S.get(url=URL, params=PARAMS)
		DATA = R.json()

		description = DATA["query"]["pages"][0]["extract"]

		card.description = description

		cards.append(card)
	
	for card in cards:
		print(card.title + "\n" + card.description + "\n" + str(card.value) + "\n")
		print("\n")
	return "Start game with " + str(numberOfPlayers) + " players"