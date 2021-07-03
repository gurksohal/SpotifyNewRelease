from pymongo import MongoClient, TEXT, DESCENDING

def createSongCollectionIndexes():
    db.new_releases.create_index([("artists.name", TEXT)])
    db.new_releases.create_index([("artists.id", DESCENDING)])
    db.new_releases.create_index([("releaseDate", DESCENDING)])

def createArtistCollectionIndexes():
    db.artists.create_index([("name", TEXT)])

def getSongsCollection():
    return db.new_releases

def getUserCollection():
    return db.users

def getArtistCollection():
    return db.artists


client = MongoClient()
db = client.newSongDB

createSongCollectionIndexes()
createArtistCollectionIndexes()
