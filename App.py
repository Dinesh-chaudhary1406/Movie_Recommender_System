import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
from concurrent.futures import ThreadPoolExecutor
import os

st.set_page_config(page_title="Movie Recommender", layout="wide")

# 🌙 Custom dark theme
st.markdown("""
    <style>
        body, .main {
            background-color: #0e1117;
            color: white;
        }
        h1 {
            color: #ff4b4b;
            text-align: center;
            font-size: 3em;
        }
        .movie-title {
            text-align: center;
            margin-top: 8px;
            font-size: 1.1em;
            color: white;
        }
        img {
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# 📥 Download similarity.pkl if missing
SIMILARITY_FILE = "similarity.pkl"
DRIVE_FILE_ID = "1oPh4MyV9ERw0plQ0gDJFC4CteWu-y6ZW"
if not os.path.exists(SIMILARITY_FILE):
    url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
    gdown.download(url, SIMILARITY_FILE, quiet=False)

# 🎬 Fetch movie poster
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        res = requests.get(url, timeout=4)
        res.raise_for_status()
        data = res.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    return "https://via.placeholder.com/500x750?text=No+Poster"

# 🔁 Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = [movies.iloc[i[0]]['title'] for i in top_movies]
    movie_ids = [movies.iloc[i[0]]['id'] for i in top_movies]

    with ThreadPoolExecutor() as executor:
        recommended_posters = list(executor.map(fetch_poster, movie_ids))

    return recommended_titles, recommended_posters

# 📦 Load Data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIMILARITY_FILE, 'rb'))

# 🔍 UI
st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("🎯 Recommend"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
