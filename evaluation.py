from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np
import plotly.graph_objects as go

#df = pd.read_csv("spotify-tracks-dataset-cleaned.csv") #Récupérer les données de notre nouveau fichier
df = pd.read_csv("spotify-tracks-dataset-enriched.csv") 

#features = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']
features_enrichies = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'mood_euphoria', 'mood_chill', 'mood_sombre', 'mood_dansant', 'groove_score', 'vocal_ratio', 'tempo_sin', 'tempo_cos', 'acoustic_instrumental'] #Trier les colonnes qui nous intéresse pour notre algorithme




def recommend_cosine (track_name):
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0: #Vérifier si la chanson qu'on choisi existe, on transforme 
        return None
    
    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]#Récupère l'index de la track (récupère que la première track en cas de doublon)
    features_track = df.iloc[idx][features_enrichies] #Récupère uniquement les features audio d'une ligne

    similarity_vector = cosine_similarity(features_track.values.reshape(1, -1), df[features_enrichies]) #Fais le calcul de similarité pour une ligne (on a reshape la ligne pour qu'elle soit converti en tableau 2D et utilsable pour la fonction cosine_similarity())
    best_score = similarity_vector[0].argsort()[-6:][::-1] #Trouver les 5 score les plus élevés et les stocker
    best_score = [i for i in best_score if i != idx][:5] 

    return df.iloc[best_score][['track_name', 'artists']], similarity_vector[0][best_score] #Retourne les 5 meilleurs musiques les plus similaires avec leurs scores


knn = NearestNeighbors(n_neighbors=6)
knn.fit(df[features_enrichies])

def recommend_knn (track_name):
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0: #Vérifier si la chanson qu'on choisi existe, on transforme 
        return None
    
    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]#Récupère l'index de la track (récupère que la première track en cas de doublon)
    features_track = df.iloc[idx][features_enrichies] #Récupère uniquement les features audio d'une ligne

    knn = NearestNeighbors(n_neighbors=6).fit(df[features_enrichies]) #Entraîner la dataset avvec KNN
    distances, indices = knn.kneighbors(features_track.values.reshape(1, -1))
    indices = indices[0]    
    indices = [i for i in indices if i != idx][:5] 

    return df.iloc[indices][['track_name', 'artists']], distances[0][:5]

def recommend_kmeans (track_name, n_clusters = 50):
    if len(df[df['track_name'].str.lower() == track_name.lower()]) == 0: #Vérifier si la chanson qu'on choisi existe, on transforme 
        return None
    
    idx = df[df['track_name'].str.lower() == track_name.lower()].index[0]#Récupère l'index de la track (récupère que la première track en cas de doublon)
    features_track = df.iloc[idx][features_enrichies] #Récupère uniquement les features audio d'une ligne

    kmean = KMeans(random_state=42, n_init=10, n_clusters=n_clusters).fit(df[features_enrichies])
    cluster_id = kmean.predict(features_track.values.reshape(1, -1))[0]
    cluster_indices = df[kmean.labels_ == cluster_id].index.tolist()  
    cluster_indices = [i for i in cluster_indices if i != idx][:5] 

    centroid = kmean.cluster_centers_[cluster_id]
    distances = np.linalg.norm(df.iloc[cluster_indices][features_enrichies].values - centroid, axis=1) #Calculer chaque track par rapport au centre pour avoir la distance de chaque track par rapport au centre du cluster

    return df.iloc[cluster_indices][['track_name', 'artists']], distances

CHANSONS_TEST = ["Blinding Lights", "Bohemian Rhapsody", "Bad Guy", "Shape of You", "Lose Yourself", "Someone Like You", "Levitating", "Watermelon Sugar"] 
MODELES = { "Cosine" : recommend_cosine,
            "KNN" : recommend_knn,
            "KMeans" : recommend_kmeans
}

def evaluate(): #Calculer les noms des musiques avec les modèles dans un nouveau DataFrame
    resultats = []
    for chanson in CHANSONS_TEST:
        recs_par_modele = {}
        for nom_modele in MODELES:
            resultat = MODELES[nom_modele](chanson)
            if resultat is not None:
                recs, scores = resultat
                recs_par_modele[nom_modele] = recs.index.tolist()
                idx_entree = df[df['track_name'].str.lower() == chanson.lower()].index[0]
                resultats.append({ "modèle" : nom_modele,
                                  "chanson" : chanson,
                                  "sim_moy" : calculer_similarite_moyenne(idx_entree, recs.index.tolist()),
                                  "diversité" : calculer_diversite_genres(recs.index.tolist()),
                                  "overlap" : None
                            })
        overlap = set(recs_par_modele["Cosine"]) & set(recs_par_modele["KNN"])
        for r in resultats[-3:]:
            r["overlap"] = len(overlap)
    return pd.DataFrame(resultats)


def calculer_diversite_genres(indices): 
    return len(df.iloc[indices]['track_genre'].unique())

def calculer_similarite_moyenne(idx_entree, indices):
    features_entree = df.iloc[idx_entree][features_enrichies]
    similarity_vector = cosine_similarity(features_entree.values.reshape(1, -1), df.iloc[indices][features_enrichies])
    return similarity_vector[0].mean()


def visualiser(): #Visualisation
    fig = go.Figure(data=[go.Scatterpolar(
        r = df_norm.loc["Cosine"].values,
        theta = ["sim_moy", "diversité", "overlap"],
        fill = 'toself',
        name="Cosine"
    ), 
    go.Scatterpolar(
        r = df_norm.loc["KNN"].values,
        theta = ["sim_moy", "diversité", "overlap"],
        fill = 'toself',
        name="KNN"
    ),
    go.Scatterpolar(
        r = df_norm.loc["KMeans"].values,
        theta = ["sim_moy", "diversité", "overlap"],
        fill = 'toself',
        name="KMeans"
    )])
    fig.show()

def visualiser_bar():
    fig = go.Figure(data=[go.Bar(
        y = df_norm.loc["Cosine"].values,
        x = ["sim_moy", "diversité", "overlap"],
        name="Cosine"
    ), 
    go.Bar(
        y = df_norm.loc["KNN"].values,
        x = ["sim_moy", "diversité", "overlap"],
        name="KNN"
    ),
    go.Bar(
        y = df_norm.loc["KMeans"].values,
        x = ["sim_moy", "diversité", "overlap"],
        name="KMeans"
    )])
    fig.show()

if __name__ == "__main__":
    df_results = evaluate()
    df_avg = df_results.groupby("modèle")[["sim_moy", "diversité", "overlap"]].mean()
    df_norm = (df_avg - df_avg.min()) / (df_avg.max() - df_avg.min())
    print(df_avg)
    visualiser_bar()