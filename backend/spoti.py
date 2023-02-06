
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from spotipy import Spotify
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os 
from os import getenv
import requests

from bs4 import BeautifulSoup

app = Flask(__name__)
load_dotenv()

# Set up CORS
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/getSample", methods=['POST'])
@cross_origin()
def getSample():
    url = "https://genius.p.rapidapi.com/search"
    sample_name = request.json['sample']

    querystring = {"q":sample_name}

    headers = {
        "X-RapidAPI-Key": getenv("rapid_api_key"),
        "X-RapidAPI-Host": "genius.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    sample_url = response.json()['response']['hits'][0]['result']['relationships_index_url']
    sample_page = requests.get(sample_url)


    soup = BeautifulSoup(sample_page.content, 'html.parser')
    sample_result = []

    for a in soup.find('section').find_all('a', href=True):
        if a.text != "Read the lyrics" and a.text != "View all":
            sample_result.append(a.text)

    print(sample_result)

    return sample_result

if __name__ == '__main__':
    app.run()