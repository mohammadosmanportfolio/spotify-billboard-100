import requests, spotipy, json, os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID") 
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET") 
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI") 

print("Which year would you like to travel to?")
date = input("Enter the date in this format YYYY-MM-DD: ")
billboard_url = "https://www.billboard.com/charts/hot-100/" + date + "/"

response = requests.get(billboard_url)

soup = BeautifulSoup(response.text, 'html.parser')
selector = "li.o-chart-results-list__item h3.c-title"
list_of_song_title_tags = soup.select(selector=selector)
list_of_song_titles = [song.text.strip() for song in list_of_song_title_tags]

spOAuth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, 
                                      redirect_uri=SPOTIPY_REDIRECT_URI,
                                      scope="playlist-modify-private")

spotify = spotipy.Spotify(oauth_manager=spOAuth)

user_id = spotify.current_user()['id']

list_of_song_uris = []
for song_title in list_of_song_titles:
    year = date[0:4]
    data = spotify.search(q=f"year:{year} track:{song_title}", type="track", limit=1)
    if len(data['tracks']['items']) == 0:
        continue
    else:
        track_uri = data['tracks']['items'][0]['uri']
        list_of_song_uris.append(track_uri)

playlist_name = date + " Billboard 100"
playlist = spotify.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist['id']

add_items = spotify.playlist_add_items(playlist_id=playlist_id, items=list_of_song_uris)
