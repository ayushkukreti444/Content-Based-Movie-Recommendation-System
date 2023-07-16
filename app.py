import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []

    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movie_list.iloc[i[0]]['movie_id']
        poster_url = fetch_poster(movie_id)
        recommended_movies.append({'title': movie_list.iloc[i[0]]['title'], 'poster': poster_url})

    return recommended_movies

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def set_image_size(image_url, width, height):
    return f'<img src="{image_url}" width="{width}" height="{height}">'

movie_list = pd.read_pickle('movie_list.pkl')
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.set_page_config(page_title='Movie Recommendation system', page_icon='🎬')

st.title('Content Based Movie Recommendation System')

st.markdown('''
    Welcome to the Content Based Movie Recommendation System! 
    Select a movie from the dropdown and click the *Search* button to get recommendations.
    Explore the recommended movies based on your selection.
''')

selected_movie = st.selectbox('Choose a movie:', movie_list['title'])

search_button = st.button('Search')

if search_button:
    recommended_movies = recommend(selected_movie)
    st.markdown('**Recommended Movies**')
    if recommended_movies:
        image_width = 100
        image_height = 200

        for movie in recommended_movies:
            st.write(movie['title'])
            st.markdown(set_image_size(movie['poster'], image_width, image_height), unsafe_allow_html=True)
    else:
        st.write('No recommendations found.')


st.markdown('---')
st.markdown('Created by Ayush Kukreti')

