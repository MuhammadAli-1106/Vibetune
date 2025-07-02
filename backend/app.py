from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
print(f"__name__ is {__name__}")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)

@app.route('/test-token')
def get_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(
        auth_url,
        data={'grant_type': 'client_credentials'},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    )
    return jsonify(auth_response.json())

if __name__ == '__main__':
    print("🚀 Flask app starting...")
    app.run(debug=True)
