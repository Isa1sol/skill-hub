from app import app
from flask import render_template
import requests

@app.route('/')
def home():
    # Chuck Norris Joke API
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke = response.json().get("value", "No joke found.")
    return render_template('index.html', joke=joke)
