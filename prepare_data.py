import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


df = pd.read_csv("spotify-tracks-dataset.csv") #Récupérer la data set en format csv

df = df[['track_name', 'artists', 'track_genre', 'danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']] #Enlever les colonnes non-neccessaires

df = df.dropna() #Supprimer les lignes où il y a des cases manquantes
df = df.drop_duplicates(subset=['track_name', 'artists']) #Supprimer les doublons
df['artists']= df['artists'].str.replace(";", ", ") #Remplace les ";" par ", " dans la colonne artiste

df['mood_euphoria'] = df['energy'] * df['valence'] #Création de nouvelles futures combinant plusieurs features existantes
df['mood_chill'] = (1- df['energy']) * df['acousticness']
df['mood_sombre']    = (1 - df['valence']) * (df['loudness'].abs() / 60)
df['mood_dansant']   = df['danceability'] * df['energy']
df['groove_score']   = df['danceability'] * (df['tempo'] / 120)
df['vocal_ratio'] = df['speechiness'] / (df['instrumentalness'] + 0.01)
df['tempo_sin'] = np.sin(2 * np.pi * df['tempo'] / 200)
df['tempo_cos'] = np.cos(2 * np.pi * df['tempo'] / 200)
df['acoustic_instrumental'] = df['acousticness'] * df['instrumentalness']


#features = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo'] #Trier les colonnes qui nous intéresse pour notre algorithme
features_enrichies = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'mood_euphoria', 'mood_chill', 'mood_sombre', 'mood_dansant', 'groove_score', 'vocal_ratio', 'tempo_sin', 'tempo_cos', 'acoustic_instrumental'] #Trier les colonnes qui nous intéresse pour notre algorithme


scaler = StandardScaler()
#df[features] = scaler.fit_transform(df[features]) #Standardiser les données (Mettre les features à la même échelle)
df[features_enrichies] = scaler.fit_transform(df[features_enrichies])

#df.to_csv("spotify-tracks-dataset-cleaned.csv", index= False) # Exporter la data set nettoyer dans nouveau fichier csv nommé "spotify-tracks-dataset-cleaned.csv"
df.to_csv("spotify-tracks-dataset-enriched.csv", index=False)



