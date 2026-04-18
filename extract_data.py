import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "87b2ceac6a784c3594cc26c87848fdd6"
CLIENT_SECRET = "dae2c24276394667baefde2e0f5797af"

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

tracks = get_tracks_from_playlist("37i9dQZEVXbIPWwFssbupI")
print(f"{len(tracks)} tracks récupérées")
print(tracks[0])
