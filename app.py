from recommender import recommend
import streamlit as st

st.title("Music Recommender") #Titre de la page
track_name = st.text_input("Tape le nom d'une chanson") #Saisit par l'utilisateur
if track_name : #Vérifier si le son saisit n'est pas nul
    result = recommend(track_name) 
    if result is None:
        st.error("Chanson non trouvée dans le dataset 😕")  #Si le son ne fait pas partie de la dataset le signaler à l'utilsateur
    else : 
        results, scores = recommend(track_name)
        st.write(results) #Afficher les 5 chansons les plus similaires