from flask import Flask
from flask import render_template
from flask import request

import requests
import random
import json

app = Flask(__name__)

runningGame = None

class Game:
	def __init__(self, cardList, teamOne, teamTwo):
		self.workingDeck = cardList
		self.teamOne = teamOne
		self.teamOneScore = 0
		self.teamTwo = teamTwo
		self.teamTwoScore = 0
		self.teamOneSolved = []
		self.teamTwoSolved = []
		self.currentCard = None

	def award_point(self, solvedCard, team):
		index = -1	
		for index, card in enumerate(self.workingDeck):
			if solvedCard.title == card.title:
				break
		if index >= len(self.workingDeck):
			return "Error: Invalid Card"

		addition = self.workingDeck[index]
		del(self.workingDeck[index])

		if team == self.teamOne:
			self.teamOneScore += addition.value
			self.teamOneSolved.append(addition)
		else:
			self.teamTwoScore += addition
			self.teamTwoSolved.append(addition)



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
	numberOfPlayers = request.args.get('p', default = 2, type = int)

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

	usedNumbers = []
	i = 0
	while i < numberOfCards:
		index = random.randint(2, 499)
		if(index in usedNumbers):
			i = i-1
			continue
		usedNumbers.append(index)
		title = MOSTVIEWED[index]["title"]
		if(not("list" in title.lower() or "user" in title.lower())):
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
		i += 1


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

	return render_template("cards.html", title = cards[0].title, description = cards[0].description, points = str(cards[0].value))
