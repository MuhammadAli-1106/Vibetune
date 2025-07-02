from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

app = Flask(__name__)

# dictionaires to store mood and activity with their corresponding valence, energy, tempo, danceability, and instrumentalness features
# mood will give baseline
# activity will tweak the values in mood 
mood_feature_map = {
    "happy": {
        "valence": 0.9,
        "energy": 0.8,
        "tempo": 120,
        "danceability": 0.8,
        "instrumentalness": 0.1
    },
    "sad": {
        "valence": 0.2,
        "energy": 0.3,
        "tempo": 70,
        "danceability": 0.3,
        "instrumentalness": 0.4
    },
    "angry": {
        "valence": 0.2,
        "energy": 0.95,
        "tempo": 130,
        "danceability": 0.6,
        "instrumentalness": 0.1
    },
    "chill": {
        "valence": 0.6,
        "energy": 0.4,
        "tempo": 85,
        "danceability": 0.6,
        "instrumentalness": 0.3
    },
    "romantic": {
        "valence": 0.8,
        "energy": 0.5,
        "tempo": 90,
        "danceability": 0.5,
        "instrumentalness": 0.2
    },
    "focused": {
        "valence": 0.5,
        "energy": 0.3,
        "tempo": 80,
        "danceability": 0.4,
        "instrumentalness": 0.7
    },
    "nostalgic": {
        "valence": 0.4,
        "energy": 0.4,
        "tempo": 75,
        "danceability": 0.5,
        "instrumentalness": 0.3
    },
    "energetic": {
        "valence": 0.8,
        "energy": 0.95,
        "tempo": 140,
        "danceability": 0.9,
        "instrumentalness": 0.1
    },
    "confident": {
        "valence": 0.85,
        "energy": 0.8,
        "tempo": 110,
        "danceability": 0.7,
        "instrumentalness": 0.2
    },
    "daydreaming": {
        "valence": 0.7,
        "energy": 0.5,
        "tempo": 85,
        "danceability": 0.5,
        "instrumentalness": 0.5
    },
    "lost": {
        "valence": 0.3,
        "energy": 0.3,
        "tempo": 65,
        "danceability": 0.4,
        "instrumentalness": 0.6
    }
}

activity_modifier = {
    "workout": {
        "energy": 0.2,
        "tempo": 20,
        "danceability": 0.1
    },
    "study": {
        "instrumentalness": 0.4,
        "energy": -0.1,
        "tempo": -10
    },
    "party": {
        "danceability": 0.2,
        "energy": 0.2,
        "valence": 0.1
    },
    "commute": {
        "tempo": 10,
        "danceability": 0.1
    },
    "sleep": {
        "energy": -0.3,
        "tempo": -20,
        "instrumentalness": 0.3
    },
    "cleaning": {
        "energy": 0.15,
        "tempo": 10,
        "danceability": 0.15
    },
    "meditation": {
        "instrumentalness": 0.5,
        "energy": -0.2,
        "tempo": -15,
        "valence": 0.1
    }
}

# combining both
def build_feature_targets(mood, activity):
    base = mood_feature_map.get(mood, {})
    modifiers = activity_modifier.get(activity, {})
    
    # dicionary to store target feature values
    combined = {}

    for feature in base:
        # If this feature is modified by the activity, apply the change
        if feature in modifiers:
            combined[f"target_{feature}"] = base[feature] + modifiers[feature]
        else:
            combined[f"target_{feature}"] = base[feature]

        # clamp the values to valid Spotify ranges (0.0 to 1.0 for most)
        if feature != "tempo":
            combined[f"target_{feature}"] = min(max(combined[f"target_{feature}"], 0.0), 1.0)

    # clamp tempo to range between 40 and 180
    if "tempo" in base:
        tempo = base["tempo"] + modifiers.get("tempo", 0)
        combined["target_tempo"] = max(40, min(tempo, 180))

    return combined


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
    app.run(debug=True)
