import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import requests
import os

st.set_page_config(layout="wide")

# Load dataset
df2 = pd.read_csv('tmdb_5000_movies.csv')

# Create a "soup" feature if not already present
if 'soup' not in df2.columns:
    df2['soup'] = df2['overview'].fillna('') + ' ' + df2['genres'].fillna('')

# Compute cosine similarity (cached for performance)
cosine_sim_file = 'cosine_sim.pkl'
if os.path.exists(cosine_sim_file):
    cosine_sim2 = pd.read_pickle(cosine_sim_file)
else:
    count_vectorizer = CountVectorizer(stop_words='english')
    count_matrix = count_vectorizer.fit_transform(df2['soup'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    pd.to_pickle(cosine_sim2, cosine_sim_file)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])

# Function to fetch movie poster
def fetch_poster(movie_title):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(url).json()
    if response['results']:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/150"

# Recommendation function
def get_recommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie_indices

# Streamlit UI
st.title("🎬 Cinematic Genius: AI-Powered Movie Recommendations")

movie_list = df2['title'].values
selected_movie = st.selectbox("Type or select a movie to get recommendation", movie_list)

if st.button("Show recommendation"):
    st.subheader(f"Top 10 Recommendations for 🎥 {selected_movie}")
    recommendations_idx = get_recommendations(selected_movie)

    cols = st.columns(5)
    for i, idx in enumerate(recommendations_idx):
        movie = df2['title'].iloc[idx]
        poster_url = fetch_poster(movie)
        overview = df2['overview'].iloc[idx] if pd.notna(df2['overview'].iloc[idx]) else "No description available."
        similarity = cosine_sim2[indices[selected_movie]][idx]

        tooltip_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="{poster_url}" style="width: 100%; border-radius: 10px;" />
            <div style="
                visibility: hidden;
                background-color: rgba(0,0,0,0.85);
                color: #fff;
                text-align: left;
                border-radius: 6px;
                padding: 10px;
                position: absolute;
                z-index: 1;
                bottom: 105%;
                left: 0;
                width: 100%;
                font-size: 12px;
                line-height: 1.4;
            " class="tooltiptext">
                <strong>{movie}</strong><br>
                <em>Similarity:</em> {similarity:.2%}<br>
                {overview[:300]}...
            </div>
        </div>
        <style>
            div:hover .tooltiptext {{
                visibility: visible;
            }}
        </style>
        """

        with cols[i % 5]:
            st.markdown(tooltip_html, unsafe_allow_html=True)
