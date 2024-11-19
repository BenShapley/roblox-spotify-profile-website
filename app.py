from flask import Flask, render_template, request
from roblox_spotify import search_robloxian2

app = Flask(__name__)

default_username = "Funky"

@app.route('/')
def index():
	my_playlist = search_robloxian2(default_username)
	return render_template('index.html', playlist_id=my_playlist, user_name=default_username)

@app.route('/', methods=['POST'])
def index_post():
	user_name = request.form['req_name']
	my_playlist = search_robloxian2(user_name)
	return render_template('index.html', playlist_id=my_playlist, user_name=user_name)