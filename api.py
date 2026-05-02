from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from recommender import recommend, df, features_enrichies
from evaluation import recommend_cosine, recommend_knn, recommend_kmeans
from spotify_api import get_track_info, get_token
from dotenv import load_dotenv
import os
import requests as req

load_dotenv()
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# GET /
# Sert le site web MusicRecommender.html directement via Flask.
# Accès : http://127.0.0.1:5001 (ne pas ouvrir le fichier HTML directement)
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return send_file("MusicRecommender.html")  # Autorise les requêtes cross-origin (nécessaire pour MusicRecommender.html)

# ─────────────────────────────────────────────
# TOKEN SPOTIFY — mis en cache pour éviter un
# nouvel appel à chaque requête (valable 1h)
# ─────────────────────────────────────────────
_token = None

def get_cached_token():
    """Retourne le token Spotify en cache, ou en génère un nouveau si absent."""
    global _token
    if _token is None:
        _token = get_token()
    return _token


# ─────────────────────────────────────────────
# GET /recommend?track=Blinding+Lights&model=cosine
# Retourne 5 recommandations pour une track donnée.
# Paramètre model : cosine (défaut) | knn | kmeans
# ─────────────────────────────────────────────
@app.route("/recommend")
def recommend_endpoint():
    track_name = request.args.get("track")
    model = request.args.get("model", "cosine")

    if not track_name:
        return jsonify({"error": "Paramètre track manquant"}), 400

    # Appel de la fonction correspondant au modèle choisi
    if model == "knn":
        result = recommend_knn(track_name)
    elif model == "kmeans":
        result = recommend_kmeans(track_name)
    else:
        result = recommend_cosine(track_name)

    if result is None:
        return jsonify({"error": "Chanson non trouvée"}), 404

    results, scores = result
    return jsonify({"tracks": results.to_dict(orient="records"), "model": model})


# ─────────────────────────────────────────────
# GET /features?track=Blinding+Lights
# Retourne les features audio d'une track (pour le radar chart).
# ─────────────────────────────────────────────
@app.route("/features")
def features_endpoint():
    track_name = request.args.get("track")

    if not track_name:
        return jsonify({"error": "Missing track"}), 400

    matches = df[df['track_name'].str.lower() == track_name.lower()]
    if len(matches) == 0:
        return jsonify({"error": "Not found"}), 404

    track = matches.iloc[0]

    # On retourne uniquement les features interprétables (échelle 0–1)
    key_features = ['danceability', 'energy', 'loudness', 'speechiness',
                    'acousticness', 'instrumentalness', 'valence']

    return jsonify({
        "features": track[key_features].to_dict(),
        "genre": str(track.get('track_genre', ''))
    })


# ─────────────────────────────────────────────
# GET /spotify_info?track=Blinding+Lights&artist=The+Weeknd
# Retourne la pochette d'album et le lien Spotify via l'endpoint /search.
# Note : /audio-features est bloqué depuis 2024, seul /search est accessible.
# ─────────────────────────────────────────────
@app.route("/spotify_info")
def spotify_info_endpoint():
    track_name = request.args.get("track")
    artist = request.args.get("artist", "")

    if not track_name:
        return jsonify({}), 400

    try:
        info = get_track_info(get_cached_token(), track_name, artist)
        return jsonify(info or {})
    except:
        # En cas d'erreur Spotify (token expiré, rate limit...), on retourne vide
        return jsonify({})


# ─────────────────────────────────────────────
# GET /genres
# Retourne la liste triée des 113 genres du dataset.
# Utilisé pour alimenter le filtre genre dans l'interface.
# ─────────────────────────────────────────────
@app.route("/genres")
def genres_endpoint():
    return jsonify({"genres": sorted(df['track_genre'].unique().tolist())})


# ─────────────────────────────────────────────
# GET /artists?genre=pop
# Retourne les artistes d'un genre donné (max 200).
# Utilisé pour alimenter le filtre artiste après sélection du genre.
# ─────────────────────────────────────────────
@app.route("/artists")
def artists_endpoint():
    genre = request.args.get("genre", "")
    if genre:
        artists = sorted(df[df['track_genre'] == genre]['artists'].unique().tolist())[:200]
    else:
        artists = []
    return jsonify({"artists": artists})


# ─────────────────────────────────────────────
# GET /search?q=blind
# Retourne jusqu'à 10 tracks dont le nom contient la saisie.
# Utilisé pour l'autocomplete dans MusicRecommender.html.
# Minimum 2 caractères pour éviter des requêtes trop larges.
# ─────────────────────────────────────────────
@app.route("/search")
def search_endpoint():
    q = request.args.get("q", "")

    if len(q) < 2:
        return jsonify({"results": []})

    # Filtrage insensible à la casse sur le nom de la track
    matches = df[df['track_name'].str.lower().str.contains(q.lower(), na=False)]
    results = matches[['track_name', 'artists']].head(10)

    return jsonify({"results": results.to_dict(orient="records")})


# ─────────────────────────────────────────────
# POST /chat
# Proxie les messages vers l'API Anthropic côté serveur.
# La clé API n'est jamais exposée au navigateur.
# Body attendu : { "messages": [...], "system": "..." }
# ─────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat_endpoint():
    body = request.get_json()
    messages = body.get("messages", [])
    system = body.get("system", "")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY manquante dans le .env"}), 500

    response = req.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-5",
            "max_tokens": 1000,
            "system": system,
            "messages": messages
        }
    )
    return jsonify(response.json())


# ─────────────────────────────────────────────
# GET /tracks?artist=Drake&genre=pop
# Retourne les tracks d'un artiste donné, filtrées par genre si précisé.
# Utilisé pour alimenter la selectbox quand genre + artiste sont sélectionnés.
# ─────────────────────────────────────────────
@app.route("/tracks")
def tracks_endpoint():
    artist = request.args.get("artist", "")
    genre = request.args.get("genre", "")

    if not artist:
        return jsonify({"tracks": []})

    mask = df['artists'] == artist
    if genre:
        mask = mask & (df['track_genre'] == genre)

    tracks = df[mask]['track_name'].dropna().unique().tolist()
    return jsonify({"tracks": sorted(tracks)})


# ─────────────────────────────────────────────
# Lancement du serveur Flask en local sur le port 5001
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(port=5001, debug=True)