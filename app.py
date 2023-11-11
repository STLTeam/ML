import streamlit as st
import pickle
import pandas as pd
import difflib
import requests



def fetch_poster(movie_id):
  response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ce365e0bb0a3897036362ade305c4a5c'.format(movie_id))
  data = response.json()
  return "https://image.tmdb.org/t/p/w500/" +  data['poster_path']


def recommend(movie):

  list_of_all_titles = movies['title'].tolist()

  find_close_match = difflib.get_close_matches(movie, list_of_all_titles)

  close_match = find_close_match[0]
  index_of_the_movie = movies[movies.title == close_match]['index'].values[0]
  similarity_score = list(enumerate(similarity[index_of_the_movie]))
  sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)

  recommended_movies = []
  recommended_movies_posters = []

  i = 1
  for movie in sorted_similar_movies[1:]:
    index = movie[0]
    title_from_index = movies[movies.index==index]['title'].values[0]
    id_from_index = movies[movies.index==index]['id'].values[0]

    if (i<6):
      recommended_movies.append(title_from_index)
      recommended_movies_posters.append(fetch_poster(id_from_index))
      i+=1
  return recommended_movies , recommended_movies_posters


movies_dict = pickle.load(open('movies2_dict.pkl' , 'rb'))
movies =pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity2.pkl' , 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    '' , movies['title'].values
)

if st.button('Recommend'):
    Names,Posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      st.text(Names[0])
      st.image(Posters[0])

    with col2:
      st.text(Names[1])
      st.image(Posters[1])

    with col3:
      st.text(Names[2])
      st.image(Posters[2])

    with col4:
      st.text(Names[3])
      st.image(Posters[3])

    with col5:
      st.text(Names[4])
      st.image(Posters[4])



