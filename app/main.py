from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home_page():
	return render_template("index.html")

@app.route('/start')
def start():
	return "Start Game"