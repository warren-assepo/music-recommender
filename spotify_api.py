import os
import base64
import json
from dotenv import load_dotenv
from requests import post, get
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token(): #Accès temporaire à l'api de de Spotify
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

token = get_token()
print(token)

def get_track_info(token, track_name, artist_name): #Prendre les informations de chaque chansons (lien et l'image du titre)
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer " + token}
    query = f"?q={track_name} {artist_name}&type=track&limit=1"
    result = get(url + query, headers=headers)
    json_result = json.loads(result.content)
    # extraire la pochette et le lien
    track = json_result['tracks']['items'][0]
    image_url = track['album']['images'][0]['url']
    spotify_url = track['external_urls']['spotify']
    return {"image": image_url, "url": spotify_url}

token = get_token()
print(get_track_info(token, "Blinding Lights", "The Weeknd"))
