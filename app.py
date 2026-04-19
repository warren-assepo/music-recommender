from recommender import recommend, df, features
import streamlit as st
import plotly.graph_objects as go

st.title("Music Recommender") #Titre de la page

track_genre = st.selectbox("Choisis le genre musical",[""] + list(df['track_genre'].unique())) #Saisit du genre par l'utilisateur
df_filtered_track_genre = df[df['track_genre'] == track_genre] if track_genre else df #On filtre notre data set par rapport au genre sélectionné

artists = st.selectbox("Choisis l'artiste",[""] + list(df_filtered_track_genre['artists'].unique())) #Saisit du genre par l'utilisateur
df_filtered_artists = df_filtered_track_genre[df_filtered_track_genre['artists'] == artists] if artists else df_filtered_track_genre #On se base du genre pour filter notre data

if artists: #Si un artiste est sélectionné on affcihe que le son et pas le nom de l'artiste dans les proposition
    options = [""] + list(df_filtered_artists['track_name'])
else:
    options = [""] + list(df_filtered_artists['track_name'] + " - " + df_filtered_artists['artists'])
    
autocomplete = st.selectbox("Tape le nom d'une chanson", options) #Propose des choix à l'utilsateur (valeur initiale nulle)
track_name = autocomplete.split(" - ")[0] 

if track_name : #Vérifier si le son saisit n'est pas nul
    result = recommend(track_name) 
    if result is None:
        st.error("Chanson non trouvée dans le dataset 😕")  #Si le son ne fait pas partie de la dataset le signaler à l'utilsateur
    else:
        results, scores = result
        track_data = df[df['track_name'].str.lower() == track_name.lower()].iloc[0]
        for idx, row in results.iterrows():
            spotify_url = f"https://open.spotify.com/search/{row['track_name']}%20{row['artists']}".replace(" ", "%20")
            st.markdown(f"[{row['track_name']} - {row['artists']}]({spotify_url})") #Afficher les 5 chansons les plus similaires et leur lien sur spotify
    
    #Affiche un radar chart pour mieux comprendre les similarités        
    fig = go.Figure(go.Scatterpolar(
        r=track_data[features].values,
        theta=features,
        fill='toself'
    ))

    st.plotly_chart(fig)


   