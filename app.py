import requests
import streamlit as st
import pickle
import pandas as pd

# Load data
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

# Create DataFrame
movies=pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    try:
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f258e8478c5a2a4c313c6f21ea7f04d0&language=en-US"
        data=requests.get(url).json()
        poster_path=data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return "https://via.placeholder.com/500"  #Placeholder image if no poster found
    except Exception as e:
        st.error(f"Error fetching poster:{e}")
        return "https://via.placeholder.com/500"  #Placeholder image on error


def recommend(movie):
    try:
        movie_index=movies[movies['title'] == movie].index[0]
        distances=similarity[movie_index]
        movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]  #0th index is the movies itself

        recommended_movies=[]
        recommended_movies_poster=[]
        for i in movies_list:
            movie_id=movies.iloc[i[0]].get('movie_id')
            if movie_id:## if to avoid  error in case of deletions
                recommended_movies_poster.append(fetch_poster(movie_id))
                recommended_movies.append(movies.iloc[i[0]].get('title'))

        return recommended_movies, recommended_movies_poster
    except Exception as e:
        st.error(f"Error recommending movies:{e}")
        return [],[] ##error msg and empty lists


st.header('Movie Recommender System')

movie_list = movies['title'].values

selected_movie_name = st.selectbox("Type or select a movie from the dropdown",movie_list)

if st.button('Show Recommendations'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)

    if recommended_movie_names:
        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
        with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])
        with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
        with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
        with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])
    else:
        st.text("No recommendations found.")
