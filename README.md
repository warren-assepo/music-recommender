# 🎵 Music Recommender System

## Description
Web application that recommends 5 similar songs based on Spotify audio features using cosine similarity.

## Demo
[Link for the demo](https://music-recommender-9x8cwickxkn7q2sw2wbick.streamlit.app/)

## Tech Stack
- Python
- Pandas
- Scikit-learn
- Streamlit

## How it works
1. Selected relevant audio features (danceability, energy, loudness, speechiness, acousticness, instrumentalness, valence, tempo, key, mode)
2. Cleaned the dataset: removed empty rows, duplicate tracks, and standardized all features using StandardScaler
3. Filter songs by genre and artist before searching
4. Autocomplete search with song name and artist to avoid confusion between songs with the same title
5. Computed cosine similarity between the selected song and all others to find the 5 most similar tracks
6. Each recommendation includes a clickable Spotify link and a radar chart of the audio features

## Dataset
Spotify Tracks Dataset from Kaggle — 83,000+ unique tracks after cleaning

## Run locally
```bash
git clone https://github.com/warren-assepo/music-recommender
cd music-recommender
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Future improvements
- Integrate the Spotify API for a real-time catalog
- Add a user feedback system to improve recommendations


## Author
Warren ASSEPO — [LinkedIn](https://www.linkedin.com/in/warren-assepo/)