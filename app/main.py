from flask import Flask
from flask import render_template
from flask import request

import requests
import random
import json

app = Flask(__name__)

runningGame = None
editedCardList = None
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
	global runningGame
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
	print(DATA)
	MOSTVIEWED = DATA["query"]["mostviewed"]
	print(MOSTVIEWED)
	usedNumbers = []
	i = 0
	while i < numberOfCards:
		index = random.randint(2, 499)
		if(index in usedNumbers):
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
			continue
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
	
	cardsJSList = []
	for card in cards:
		cardsJSList.append(card.__dict__)
		print(card.title + "\n" + card.description + "\n" + str(card.value) + "\n")
		print("\n")

	cardsJavascriptString = json.dumps(cardsJSList)

	runningGame = Game(cards, "Team 1", "Team 2")
	return render_template("cards.html", title = cards[0].title, description = cards[0].description, points = str(cards[0].value), cards = cardsJavascriptString)

@app.route('/play/<jsdata>')
def playGame(jsdata):
	global runningGame
	global editedCardList
	newCardList = []
	jsdata = jsdata.split(",")
	for value in jsdata:
		print(value)
		newCardList.append(runningGame.workingDeck[int(value)])
	runningGame.workingDeck = newCardList
	editedCardList = newCardList

	cardsJSList = []
	for card in newCardList:
		cardsJSList.append(card.__dict__)
	
	cardsJavascriptString = json.dumps(cardsJSList)

	return render_template("play.html", cards = cardsJavascriptString)

@app.route('/playGame')
def playGameReturnRenderTemplate():
	global runningGame
	global editedCardList

	cardsJSList = []
	for card in editedCardList:
		cardsJSList.append(card.__dict__)

	cardsJavascriptString = json.dumps(cardsJSList)
	return render_template("play.html", cards = cardsJavascriptString)