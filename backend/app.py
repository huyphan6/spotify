from flask import Flask, request, jsonify
from flask_cors import CORS
from spotipy import Spotify
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv
import os 

app = Flask(__name__)
load_dotenv()

# Set up CORS
CORS(app)

# Set up Spotify API client
client_id = os.getenv("clientID")
client_secret = os.getenv("clientSECRET")
userID = os.getenv("userID")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(client_credentials_manager=client_credentials_manager)

@app.route("/create_playlist<mood>", methods=['POST'])
def create_playlist(mood):
    # Authenticate with Spotify API
    sp = Spotify(auth=util.prompt_for_user_token(userID, "playlist-modify-public"))
    
    # Search for tracks based on mood
    results = sp.search(mood, 'track', 5)
    track_ids = [t['id'] for t in results['tracks']['items']]
    
    # Create a playlist based on mood
    playlist = sp.user_playlist_create(userID, mood + " playlist")
    sp.user_playlist_add_tracks(userID, playlist['id'], track_ids)
    
    return "Playlist created successfully!"

@app.route("/get_playlist", methods=['GET'])
def get_playlist(mood):
    # Authenticate with Spotify API
    sp = Spotify(auth=util.prompt_for_user_token(userID, "playlist-read-private"))

    # Get the user's playlists
    playlists = sp.current_user_playlists()

    # Find the playlist with the given mood
    playlist = next((p for p in playlists['items'] if p['name'] == mood + " playlist"), None)
    if playlist is None:
        return "Playlist not found", 404
    
    # Get the tracks of the playlist
    tracks = sp.playlist_tracks(playlist['id'])

    # Return the playlist as a JSON object
    return jsonify(tracks)

# Route for creating a playlist
# @app.route('/create-playlist', methods=['GET'])
# def create_playlist():
#     # Get mood from request body
#     mood = request.json['mood']
    
#     # Query Spotify API for tracks based on mood
#     results = sp.search(mood, 'track', 5)
    
#     # Get list of track URIs from search results
#     track_uris = [track['uri'] for track in results['tracks']['items']]
    
#     # Create a new playlist in user's Spotify account
#     playlist = sp.user_playlist_create(userID, mood + " Playlist")
    
#     # Add tracks to the new playlist
#     sp.user_playlist_add_tracks(userID, playlist['id'], track_uris)
    
#     # Return the playlist details
#     return jsonify(playlist)

if __name__ == '__main__':
    app.run()
