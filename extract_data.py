import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "ton_client_id"
CLIENT_SECRET = "ton_client_secret"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

print("Connexion réussie ✅")

def get_tracks_from_playlist(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    for item in results['items']:
        track = item['track']
        if track:
            tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name']
            })
    return tracks

tracks = get_tracks_from_playlist("ton_client_secret")
print(f"{len(tracks)} tracks récupérées")
print(tracks[0])
