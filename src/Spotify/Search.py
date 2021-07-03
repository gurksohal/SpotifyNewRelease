import datetime

from Data import ArtistCollection
from Models.Artist import Artist
from Spotify.API import sp

def artistSearch(searchString):
    result = sp.search(q=searchString, limit=50, type="artist")
    artistList = []
    for data in result["artists"]["items"]:
        try:
            artistList.append(Artist(data).__dict__)
        except KeyError or TypeError:
            log("Unable to create Artist object.")

    ArtistCollection.write(artistList)


def log(msg):
    print("[{}] {}".format(datetime.datetime.now(), msg))
