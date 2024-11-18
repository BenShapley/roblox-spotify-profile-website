from flask import Flask, render_template, request
from roblox_spotify import search_robloxian2
# app is a variable representing 
# our flask app
# __name__ is a python reserved 
# word
# telling Flask where our code
# lives
app = Flask(__name__)

default_username = "Funky"

# set up our landing page
@app.route('/')
def index():
	my_playlist = search_robloxian2(default_username)
	return render_template('index.html', playlist_id=my_playlist, user_name=default_username)

# only use this when posting data!
@app.route('/', methods=['POST'])
def index_post():
	user_name = request.form['req_name']
	my_playlist = search_robloxian2(user_name)
	return render_template('index.html', playlist_id=my_playlist, user_name=user_name)