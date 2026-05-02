from recommender import recommend, df, features_enrichies
import streamlit as st
import plotly.graph_objects as go
from spotify_api import get_track_info, get_token

token = get_token()

st.title("Music Recommender") #Titre de la page

st.markdown("##### 🎵 Découvre des sons similaires basés sur les features audio Spotify") 

st.markdown("""
<style>
    .stApp {
        background-color: #121212;
    }
    .stSelectbox label {
        color: #1DB954 !important;
        font-weight: bold;
    }
    .stMarkdown a {
        color: #1DB954 !important;
        text-decoration: none;
        font-size: 16px;
    }
    .stMarkdown a:hover {
        color: white !important;
    }
    h1 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True) #Ajout de style avec du CSS

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
        info_entree = get_track_info(token, track_name, track_data['artists'])
        if info_entree:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(info_entree['image'], width=60)
            with col2:
                st.markdown(f"**[{track_name} - {track_data['artists']}]({info_entree['url']})**")
        for idx, row in results.iterrows():
            spotify_url = f"https://open.spotify.com/search/{row['track_name']}%20{row['artists']}".replace(" ", "%20")
            info = get_track_info(token, row['track_name'], row['artists'])
            if info:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(info['image'], width=60)
                with col2:
                    st.markdown(f"[{row['track_name']} - {row['artists']}]({info['url']})")
    
    #Affiche un radar chart pour mieux comprendre les similarités   
    radar_data = (track_data[features_enrichies] - track_data[features_enrichies].min()) / (track_data[features_enrichies].max() - track_data[features_enrichies].min())
    fig = go.Figure(go.Scatterpolar(
        r=radar_data.values,
        theta=features_enrichies,
        fill='toself'
    ))

    st.plotly_chart(fig)


   