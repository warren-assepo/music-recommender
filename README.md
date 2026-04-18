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
3. For each song searched, computed cosine similarity between that song and all others in the dataset to find the 5 most similar tracks

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
- Allow search by artist + title to avoid song name conflicts
- Add a radar chart of audio features for each recommendation

## Author
Warren ASSEPO — [LinkedIn](https://www.linkedin.com/in/warren-assepo/)