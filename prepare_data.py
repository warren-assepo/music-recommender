import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("spotify-tracks-dataset.csv") #Récupérer la data set en format csv

df = df[['track_name', 'artists', 'track_genre', 'danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']] #Enlever les colonnes non-neccessaires

df = df.dropna() #Supprimer les lignes où il y a des cases manquantes
df = df.drop_duplicates(subset=['track_name', 'artists']) #Supprimer les lignes où il y a des doublons
df['artists']= df['artists'].str.replace(";", ", ") #Remplace les ";" par ", " dans la colonne artiste


features = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo'] #Trier les colonnes qui nous intéresse pour notre algorithme

scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features]) #Standardiser les données (Mettre les features à la même échelle)

df.to_csv("spotify-tracks-dataset-cleaned.csv", index= False) # Exporter la data set nettoyer dans nouveau fichier csv nommé "spotify-tracks-dataset-cleaned.csv"



