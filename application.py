import streamlit as st
import pandas as pd
import requests
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df2 = pd.read_csv("tmdb_5000_movies.csv")

# Clean NaNs
df2['overview'] = df2['overview'].fillna('')
df2['genres'] = df2['genres'].fillna('[]')
df2['release_date'] = df2['release_date'].fillna('Unknown')

# Convert genres string to list of names
def extract_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        return ', '.join([g['name'] for g in genres])
    except:
        return 'Unknown'

df2['clean_genres'] = df2['genres'].apply(extract_genres)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df2['overview'])

# Cosine similarity
cosine_sim2 = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Index mapping
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

# Function to fetch posters
def fetch_poster(title):
    try:
        api_key = '823c5958046cde573b62665a52cf8c88'
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url)
        data = response.json()
        poster_path = data['results'][0]['poster_path'] if data['results'] else None
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# Recommender function
def recommend(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim2[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10
    movie_indices = [i[0] for i in sim_scores]
    return movie_indices

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Cinematic Genius: AI-Powered Movie Recommendations")
st.write("Enter a movie title to get similar movie recommendations based on description and genre.")

selected_movie = st.selectbox("Type or select a movie", df2['title'].sort_values().unique())

if st.button("Show recommendation"):
    recommendations_idx = recommend(selected_movie)

    st.subheader(f"Top 10 Recommendations for 🎥 **{selected_movie}**")

    cols = st.columns(5)
    for i, idx in enumerate(recommendations_idx):
        movie = df2['title'].iloc[idx]
        poster_url = fetch_poster(movie)
        overview = df2['overview'].iloc[idx] if pd.notna(df2['overview'].iloc[idx]) else "No description available."
        genres = df2['clean_genres'].iloc[idx]
        release = df2['release_date'].iloc[idx]

        with cols[i % 5]:
            st.image(poster_url, caption=f"{movie}", use_container_width=True)
            with st.expander("ℹ️ More Info"):
                st.markdown(f"**Rank {i + 1} {'🔥' if i == 0 else ''}**")
                st.markdown(f"**Genres:** {genres}")
                st.markdown(f"**Release Date:** {release}")
                st.markdown(f"**Description:** {overview}")
