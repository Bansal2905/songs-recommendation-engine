# Importing necessary libraries
import pickle
import Preprocessor
import streamlit as st
import numpy as np
import pandas as pd
import json
st.set_page_config(layout="wide")
# Reading the data
df_triplets = pd.read_csv("triplets_file.csv")
df_songs = pd.read_csv("song_data.csv")

# Opening user_matrix
with open('user_matrix.pkl', 'rb') as file:
    user_matrix = pickle.load(file)
# Opening song_matrix
with open('song_matrix.pkl', 'rb') as file:
    song_matrix = pickle.load(file)
# Opening user index
with open('user_index.json', 'r') as json_file:
    user_index = json.load(json_file)
# Opening song index
with open('songs_index.json', 'r') as json_file:
    songs_index = json.load(json_file)

# streamlte page
st.title("Song Recommendation engine")
recommendation = st.sidebar.selectbox('Select type of recommendation',("Type I","Type II"))
if recommendation ==  "Type I":
    st.title("Type I Recommendation")
    st.header("This type of recommendation is based on user behaviour. The model predicts the similar users and recommends most listened songs for those users.")
    # Taking input from user
    number = st.number_input('Insert the user number',min_value = 1,max_value = user_matrix.shape[0])
    # # Finding nearest five users
    nearest_users = np.argsort(Preprocessor.distance_from_remaining_users(user_matrix[number],user_matrix))[1:6]
    nearest_users_key = []
    for i in nearest_users:
        nearest_users_key = nearest_users_key + Preprocessor.get_keys_by_value(user_index, i)
    if st.button('Recommend',type="primary"):
        st.header(f"Top 5 nearest users to user {number} are")
        st.write(nearest_users_key)
        st.header("Most listened songs heared by these users")
        top_songs = list(df_triplets[df_triplets["user_id"].isin(nearest_users_key)].drop_duplicates(subset = "song_id").sort_values(by = "listen_count",ascending = False).iloc[:10,1])
        st.write(df_songs[df_songs["song_id"].isin(top_songs)].drop_duplicates(subset = "song_id")["title"].values)
unique_songs = list(df_songs[df_songs["song_id"].isin(list(songs_index.keys()))]["title"].unique())
if recommendation ==  "Type II":
    st.title("Type II Recommendation")
    st.header("This type of recommendation is based on songs. The model predicts the similar songs and suggestes the nearest songs based on euclidean distance")
    # Taking input from user
    selected_song = st.selectbox("Select songs",unique_songs)
    selected_song_id = df_songs[df_songs["title"] == selected_song]["song_id"].values[0]
    # st.write(selected_song_id)
    selected_song_index = songs_index[selected_song_id]
    # st.write(selected_song_index)
    nearest_songs = np.argsort(Preprocessor.distance_from_remaining_users(song_matrix[selected_song_index],song_matrix))[1:6]
    nearest_songs_key = []
    for i in nearest_songs:
        nearest_songs_key = nearest_songs_key + Preprocessor.get_keys_by_value(songs_index, i)
    top_songs = list(df_triplets[df_triplets["song_id"].isin(nearest_songs_key)].drop_duplicates(subset = "song_id").sort_values(by = "listen_count",ascending = False).iloc[:10,1])
    if st.button('Recommend',type="primary"):
        st.header(f"Top 10 closest songs are")
        st.write(df_songs[df_songs["song_id"].isin(top_songs)].drop_duplicates(subset = "song_id")["title"].values)


