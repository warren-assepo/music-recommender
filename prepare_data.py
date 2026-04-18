import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("spotify-tracks-dataset.csv") #Récupérer la data set en format csv
print(df.head())

df = df[['track_name', 'artists', 'danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']] #Enlever les colonnes non-neccessaires
print(df.head())
print(len(df))
df = df.dropna() #Supprimer les lignes où il y a des cases manquantes
print(len(df))
df = df.drop_duplicates(subset=['track_name', 'artists']) #Supprimer les lignes où il y a des doublons
print(len(df))



features = ['danceability', 'energy', 'loudness', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo'] #Trier les colonnes qui nous intéresse pour notre algorithme
print(features)
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features]) #Standardiser les données (Mettre les features à la même échelle)
print(df.head())
df.to_csv("spotify-tracks-dataset-cleaned.csv", index= False) # Exporter la data set nettoyer dans nouveau fichier csv nommé "spotify-tracks-dataset-cleaned.csv"



