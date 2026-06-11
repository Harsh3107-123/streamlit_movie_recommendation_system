import streamlit as st
import pandas as pd
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #141414;
}

h1 {
    color: #E50914;
    text-align: center;
}

.stSelectbox label {
    color: white !important;
    font-size: 18px;
}

.movie-title {
    text-align: center;
    color: white;
    font-size: 15px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

movie_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=42b746e3c0b258eb73c85563897d7b72&language=en-US"

        response = requests.get(url)
        data = response.json()

        if data.get("poster_path"):
            return (
                "https://image.tmdb.org/t/p/w500/"
                + data["poster_path"]
            )

    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Choose a Movie",
    movies["title"].values
)

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    st.subheader("Recommended For You 🍿")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_container_width=True)
        st.markdown(
            f"<p class='movie-title'>{names[0]}</p>",
            unsafe_allow_html=True
        )

    with col2:
        st.image(posters[1], use_container_width=True)
        st.markdown(
            f"<p class='movie-title'>{names[1]}</p>",
            unsafe_allow_html=True
        )

    with col3:
        st.image(posters[2], use_container_width=True)
        st.markdown(
            f"<p class='movie-title'>{names[2]}</p>",
            unsafe_allow_html=True
        )

    with col4:
        st.image(posters[3], use_container_width=True)
        st.markdown(
            f"<p class='movie-title'>{names[3]}</p>",
            unsafe_allow_html=True
        )

    with col5:
        st.image(posters[4], use_container_width=True)
        st.markdown(
            f"<p class='movie-title'>{names[4]}</p>",
            unsafe_allow_html=True
        )
