import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components


# Function to Fetch Poster via OMDb API

def fetch_poster_by_title(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=908e115"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except Exception as e:
        print(f"❌ Failed to fetch poster for '{movie_title}': {e}")
        return "https://via.placeholder.com/500x750?text=Error"


# Load Movie Data

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Streamlit UI

st.set_page_config(page_title="🎬 OMDb Movie Recommender", layout="wide")
st.header("🎥 Movie Recommender System")


# Carousel with Sample Posters

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

sample_titles = [
    "Inception", "The Dark Knight", "Avengers: Endgame",
    "Titanic", "Fight Club", "The Matrix", "Forrest Gump", "Gladiator"
]
carousel_posters = [fetch_poster_by_title(title) for title in sample_titles]

imageCarouselComponent(imageUrls=carousel_posters, height=250)


# Movie Selection Dropdown

selectvalue = st.selectbox("🎬 Choose a movie:", movies_list)


# Recommender Function (Using Movie Title)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster_by_title(title))
    return recommended_movies, recommended_posters


# Show Recommendations

if st.button("🎯 Show Recommendations"):
    names, posters = recommend(selectvalue)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"**{names[i]}**")
