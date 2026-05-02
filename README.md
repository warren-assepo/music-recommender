# 🎵 Music Recommender System

A music recommendation web app deployed on 83,000+ Spotify tracks. Compares 3 ML models and exposes a REST API consumed by both a Streamlit interface and a standalone HTML/JS website.

## 🔗 Demo

| Interface | URL |
|---|---|
| Site web (Flask + HTML) | https://music-recommender-e6la.onrender.com |
| App Streamlit | https://music-recommender-9x8cwickxkn7q2sw2wbick.streamlit.app |
| API REST | https://music-recommender-e6la.onrender.com/recommend?track=Blinding+Lights&model=cosine |

---

## 🏗️ Architecture

```
music-recommender/
├── prepare_data.py                       # Feature engineering (10 → 18 features)
├── recommender.py                        # Cosine similarity
├── evaluation.py                         # 3 models comparison
├── api.py                                # Flask REST API
├── spotify_api.py                        # Spotify /search endpoint
├── app.py                                # Streamlit interface
├── MusicRecommender.html                 # Standalone HTML/JS website
├── spotify-tracks-dataset-enriched.csv  # 83k tracks, 18 features
└── models/
    └── kmeans_model.pkl                  # Pre-trained K-Means (joblib)
```

---

## 🤖 Models

Three recommendation algorithms compared on 8 test songs with 3 proxy metrics:

| Model | Avg Similarity | Genre Diversity | Overlap |
|-------|---------------|-----------------|---------|
| **Cosine** | **0.977** | 3.875 | 3.625 |
| KNN | 0.975 | **4.750** | 3.625 |
| K-Means | 0.774 | 1.250 | 3.625 |

**Cosine retained** for its audio precision. KNN available for genre diversity. K-Means for exploration.

> Without user feedback data, objective evaluation is the core challenge of recommendation systems (cold start problem). These proxy metrics measure audio similarity and genre diversity as approximations.

---

## ⚙️ Feature Engineering

Extended the original 10 Spotify audio features to **18 engineered features**:

```python
# Composite mood scores
df['mood_euphoria']  = df['energy'] * df['valence']
df['mood_chill']     = (1 - df['energy']) * df['acousticness']
df['mood_sombre']    = (1 - df['valence']) * (abs(df['loudness']) / 60)
df['mood_dansant']   = df['danceability'] * df['energy']
df['groove_score']   = df['danceability'] * (df['tempo'] / 200)

# Cyclic tempo encoding (captures musical periodicity)
df['tempo_sin'] = np.sin(2 * np.pi * df['tempo'] / 200)
df['tempo_cos'] = np.cos(2 * np.pi * df['tempo'] / 200)

# Interaction features
df['vocal_ratio']          = df['speechiness'] / (df['instrumentalness'] + 0.01)
df['acoustic_instrumental'] = df['acousticness'] * df['instrumentalness']
```

---

## 🔌 API Endpoints

```
GET  /                                          → Serves MusicRecommender.html
GET  /recommend?track=Blinding+Lights&model=cosine  → 5 recommendations (cosine | knn | kmeans)
GET  /features?track=Blinding+Lights            → Audio features for radar chart
GET  /spotify_info?track=X&artist=Y             → Album cover + Spotify link
GET  /genres                                    → List of 113 genres
GET  /artists?genre=pop                         → Artists filtered by genre
GET  /tracks?artist=Drake&genre=pop             → Tracks filtered by artist
GET  /search?q=blind                            → Autocomplete (min 2 chars, 10 results)
POST /chat                                      → Claude AI music assistant proxy
```

---

## 🚀 Run locally

```bash
git clone https://github.com/warren-assepo/music-recommender
cd music-recommender
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
ANTHROPIC_API_KEY=your_api_key
```

```bash
# Start Flask API + website
python api.py
# → http://127.0.0.1:5001

# Or start Streamlit app
streamlit run app.py
```

---

## 📊 Dataset

Spotify Tracks Dataset from Kaggle — **83,881 unique tracks** across 113 genres after cleaning and feature engineering.

---

## ⚠️ Known Limitations

- Static dataset (Kaggle 2023) — new releases not included
- Spotify `/audio-features` endpoint blocked since 2024 — album covers retrieved via `/search` only
- No user feedback data — evaluation relies on proxy metrics only

---

## 👤 Author

**Warren ASSEPO** — Big Data & ML student at EFREI Paris  
[LinkedIn](https://www.linkedin.com/in/warren-assepo/) · [GitHub](https://github.com/warren-assepo)
