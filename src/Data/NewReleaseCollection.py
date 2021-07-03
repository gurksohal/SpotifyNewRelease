from Data import DBConnector
from pymongo.errors import BulkWriteError
from pymongo import DESCENDING

PAGE_LIMIT = 20
collection = DBConnector.getSongsCollection()


def write(docs):
    if len(docs) <= 0:
        return False
    try:
        collection.insert_many(docs)
    except BulkWriteError:
        return False
    return True


def read(page, search, listOfIDS=None):
    if listOfIDS and len(listOfIDS) >= 0:
        res = readFollowingReleases(page, search, listOfIDS)
    else:
        res = readAllReleases(page, search)

    returnList = []
    for doc in res:
        returnList.append(doc)

    return returnList

def readAllReleases(page, search):
    skip = (page - 1) * PAGE_LIMIT
    filterObject = None
    if len(search) > 0:
        search = "\"" + search + "\""
        filterObject = {"$text": {"$search": search, "$diacriticSensitive": True}}

    return collection.find(filter=filterObject, skip=skip, limit=PAGE_LIMIT, sort=[('releaseDate', DESCENDING)])

def readFollowingReleases(page, search, listOfIDS):
    skip = (page - 1) * PAGE_LIMIT
    filterObject = {"artists.id": {"$in": listOfIDS}}
    if len(search) > 0:
        search = "\"" + search + "\""
        filterObject["$text"] = {"$search": search, "$diacriticSensitive": True}

    return collection.find(filter=filterObject, skip=skip, limit=PAGE_LIMIT, sort=[('releaseDate', DESCENDING)])
