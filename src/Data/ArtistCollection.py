from pymongo import DESCENDING
from pymongo.errors import BulkWriteError

from Data import DBConnector

collection = DBConnector.getArtistCollection()


def write(docs):
    try:
        collection.insert_many(documents=docs, ordered=False)
    except BulkWriteError:
        pass


def contains(artistID):
    artist = collection.find_one({"_id": artistID})
    return artist is not None


def searchArtist(searchString):
    searchString = "\"" + searchString + "\""
    filterObject = {"$text": {"$search": searchString, "$diacriticSensitive": True}}
    res = collection.find(filter=filterObject, limit=20, sort=[('popularity', DESCENDING)])
    returnList = []
    for doc in res:
        returnList.append(doc)

    return returnList


def getArtist(listOfIDS):
    res = collection.find({"_id": {"$in": listOfIDS}})
    returnList = []
    for doc in res:
        returnList.append(doc)

    return returnList
