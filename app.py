from recommender import recommend
from recommender import df
import streamlit as st

st.title("Music Recommender") #Titre de la page

track_genre = st.selectbox("Choisis le genre musical",[""] + list(df['track_genre'].unique())) #Saisit du genre par l'utilisateur
df_filtered_track_genre = df[df['track_genre'] == track_genre] if track_genre else df #On filtre notre data set par rapport au genre sélectionné

artists = st.selectbox("Choisis l'artiste",[""] + list(df_filtered_track_genre['artists'].unique())) #Saisit du genre par l'utilisateur
df_filtered_artists = df_filtered_track_genre[df_filtered_track_genre['artists'] == artists] if artists else df_filtered_track_genre #On se base du genre pour filter notre data

#track_name = st.text_input("Tape le nom d'une chanson") #Saisit par l'utilisateur
options = [""] + list(df_filtered_artists['track_name'] + " - " + df_filtered_artists['artists']) 
autocomplete = st.selectbox("Tape le nom d'une chanson", options) #Propose des choix à l'utilsateur (valeur initiale nulle)
track_name = autocomplete.split(" - ")[0] 

if track_name : #Vérifier si le son saisit n'est pas nul
    result = recommend(track_name) 
    if result is None:
        st.error("Chanson non trouvée dans le dataset 😕")  #Si le son ne fait pas partie de la dataset le signaler à l'utilsateur
    else:
        results, scores = result
        for idx, row in results.iterrows():
            spotify_url = f"https://open.spotify.com/search/{row['track_name']}%20{row['artists']}".replace(" ", "%20")
            st.markdown(f"[{row['track_name']} - {row['artists']}]({spotify_url})") #Afficher les 5 chansons les plus similaires


   