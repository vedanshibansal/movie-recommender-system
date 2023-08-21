import streamlit as st
import pickle
import pandas as pd
import requests
import webbrowser

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url('https://i.teknolojioku.com/2/1280/720/storage/files/images/2023/03/14/netflix-dizileri-b2tj-cover-jh1F_cover.png');
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
color: #ffffff;
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=f41b7c12388bc5320b35601979d40efa&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_ids = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_ids, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Create a homepage-like interface
st.title('Movie Reel Navigator')
st.write("Welcome to our movie recommendation platform! Choose a movie to get started.")

selected_movie_name = st.selectbox("Select a Movie", movies['title'].values)

if st.button('Recommend'):
    names, recommended_movie_ids, posters = recommend(selected_movie_name)

    num_columns = 5
    # Define the number of columns
    num_movies = len(names)
    num_rows = -(-num_movies // num_columns)
    # Calculate the number of rows needed
    cols = st.columns(num_columns)
    # Create columns based on the number of columns
    for i in range(num_movies):
        with cols[i % num_columns]:
            st.text(names[i])
            st.image(posters[i])
            tmdb_url = f"https://www.themoviedb.org/movie/{recommended_movie_ids[i]}"
            st.markdown(f"[View on TMDB]( {tmdb_url})", unsafe_allow_html=True)


st.markdown("---")
st.write(f"Created by Vedanshi Bansal | Connect on:")
linkedin_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/800px-LinkedIn_logo_initials.png"
linkedin_url = "https://www.linkedin.com/in/vedanshi-bansal-69729722b/"
st.markdown(f"[<img src='{linkedin_icon}' width='25'>]({linkedin_url})", unsafe_allow_html=True)
github_icon = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
github_url = "https://github.com/vedanshibansal"
st.markdown(f"[<img src='{github_icon}' width='25'>]({github_url})", unsafe_allow_html=True)

