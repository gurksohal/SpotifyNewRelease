import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

clientID = ""
clientSecret = ""
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=clientID,
                                                           client_secret=clientSecret))