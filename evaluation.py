from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import os

df = pd.read_csv("spotify-tracks-dataset-enriched.csv")

features_enrichies = [
    'danceability', 'energy', 'loudness', 'key', 'mode',
    'speechiness', 'acousticness', 'instrumentalness', 'valence',
    'mood_euphoria', 'mood_chill', 'mood_sombre', 'mood_dansant',
    'groove_score', 'vocal_ratio', 'tempo_sin', 'tempo_cos',
    'acoustic_instrumental'
]

# ── KNN — entraîné une seule fois au chargement du module ──
knn = NearestNeighbors(n_neighbors=6)
knn.fit(df[features_enrichies])

# ── KMEANS — entraîné une seule fois, sauvegardé sur disque avec joblib ──
# Sur Render : entraîné au premier démarrage, rechargé ensuite depuis le fichier
KMEANS_PATH = "models/kmeans_model.pkl"

if os.path.exists(KMEANS_PATH):
    kmeans = joblib.load(KMEANS_PATH)
else:
    os.makedirs("models", exist_ok=True)
    kmeans = KMeans(n_clusters=50, random_state=42, n_init=10)
    kmeans.fit(df[features_enrichies])
    joblib.dump(kmeans, KMEANS_PATH)


def recommend_cosine(track_name):
    """Recommande 5 tracks via similarité cosinus."""
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0:
        return None

    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]
    features_track = df.iloc[idx][features_enrichies]

    similarity_vector = cosine_similarity(
        features_track.values.reshape(1, -1), df[features_enrichies]
    )
    best_score = similarity_vector[0].argsort()[-6:][::-1]
    best_score = [i for i in best_score if i != idx][:5]

    return df.iloc[best_score][['track_name', 'artists']], similarity_vector[0][best_score]


def recommend_knn(track_name):
    """Recommande 5 tracks via K-Nearest Neighbors (modèle pré-entraîné)."""
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0:
        return None

    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]
    features_track = df.iloc[idx][features_enrichies]

    # Utilise le modèle KNN entraîné au chargement du module
    distances, indices = knn.kneighbors(features_track.values.reshape(1, -1))
    indices = indices[0]
    indices = [i for i in indices if i != idx][:5]

    return df.iloc[indices][['track_name', 'artists']], distances[0][:5]


def recommend_kmeans(track_name, n_clusters=50):
    """Recommande 5 tracks via K-Means (modèle pré-entraîné, chargé depuis joblib)."""
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0:
        return None

    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]
    features_track = df.iloc[idx][features_enrichies]

    # Utilise le modèle KMeans pré-entraîné — pas de .fit() à chaque appel
    cluster_id = kmeans.predict(features_track.values.reshape(1, -1))[0]
    cluster_indices = df[kmeans.labels_ == cluster_id].index.tolist()
    cluster_indices = [i for i in cluster_indices if i != idx][:5]

    centroid = kmeans.cluster_centers_[cluster_id]
    distances = np.linalg.norm(
        df.iloc[cluster_indices][features_enrichies].values - centroid, axis=1
    )

    return df.iloc[cluster_indices][['track_name', 'artists']], distances


# ── ÉVALUATION ──
CHANSONS_TEST = [
    "Blinding Lights", "Bohemian Rhapsody", "Bad Guy", "Shape of You",
    "Lose Yourself", "Someone Like You", "Levitating", "Watermelon Sugar"
]
MODELES = {
    "Cosine": recommend_cosine,
    "KNN": recommend_knn,
    "KMeans": recommend_kmeans
}


def calculer_diversite_genres(indices):
    return len(df.iloc[indices]['track_genre'].unique())


def calculer_similarite_moyenne(idx_entree, indices):
    features_entree = df.iloc[idx_entree][features_enrichies]
    similarity_vector = cosine_similarity(
        features_entree.values.reshape(1, -1),
        df.iloc[indices][features_enrichies]
    )
    return similarity_vector[0].mean()


def evaluate():
    resultats = []
    for chanson in CHANSONS_TEST:
        recs_par_modele = {}
        for nom_modele in MODELES:
            resultat = MODELES[nom_modele](chanson)
            if resultat is not None:
                recs, scores = resultat
                recs_par_modele[nom_modele] = recs.index.tolist()
                idx_entree = df[df['track_name'].str.lower() == chanson.lower()].index[0]
                resultats.append({
                    "modèle": nom_modele,
                    "chanson": chanson,
                    "sim_moy": calculer_similarite_moyenne(idx_entree, recs.index.tolist()),
                    "diversité": calculer_diversite_genres(recs.index.tolist()),
                    "overlap": None
                })
        overlap = set(recs_par_modele.get("Cosine", [])) & set(recs_par_modele.get("KNN", []))
        for r in resultats[-3:]:
            r["overlap"] = len(overlap)
    return pd.DataFrame(resultats)


def visualiser_bar():
    fig = go.Figure(data=[
        go.Bar(y=df_norm.loc["Cosine"].values, x=["sim_moy", "diversité", "overlap"], name="Cosine"),
        go.Bar(y=df_norm.loc["KNN"].values,    x=["sim_moy", "diversité", "overlap"], name="KNN"),
        go.Bar(y=df_norm.loc["KMeans"].values, x=["sim_moy", "diversité", "overlap"], name="KMeans"),
    ])
    fig.show()


if __name__ == "__main__":
    df_results = evaluate()
    df_avg = df_results.groupby("modèle")[["sim_moy", "diversité", "overlap"]].mean()
    df_norm = (df_avg - df_avg.min()) / (df_avg.max() - df_avg.min())
    print(df_avg)
    visualiser_bar()
