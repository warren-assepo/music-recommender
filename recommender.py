import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("spotify-tracks-dataset-cleaned.csv") #Récupérer les données de notre nouveau fichier
print(df.head())
features = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo'] #Trier les colonnes qui nous intéresse pour notre algorithme
"similarity_matrix = cosine_similarity(df[features]) #Matrice 113 999 x 113 999 (impossible à lancer)"

def recommend (track_name):
    if len(df[df['track_name'] == track_name]) == 0: #Vérifier si la chanson qu'on choisi existe
        return None 
    idx = df[df['track_name'] == track_name].index[0]#Récupère l'index de la track (récupère que la première track en cas de doublon)
    features_track = df.iloc[idx][features] #Récupère uniquement les features audio d'une ligne
    similarity_vector = cosine_similarity(features_track.values.reshape(1, -1), df[features]) #Fais le calcul de similarité pour une ligne (on a reshape la ligne pour qu'elle soit converti en tableau 2D et utilsable pour la fonction cosine_similarity())
    best_score = similarity_vector[0].argsort()[-6:][::-1] #Trouver les 5 score les plus élevés et les stocker
    best_score = [i for i in best_score if i != idx][:5] 

    """result = [] #Version plus longue
    for i in best_score:
        if i != idx:
            result.append(i)
    result = result[:5]""" 
    return df.iloc[best_score][['track_name', 'artists']], similarity_vector[0][best_score] #Retourne les 5 meilleurs musiques les plus similaires avec leurs scores

print(recommend("Comedy"))
print(recommend("Une chanson qui n'existe pas"))