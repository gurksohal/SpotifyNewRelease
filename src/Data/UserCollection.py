from Data import DBConnector

collection = DBConnector.getUserCollection()


def contains(username):
    user = collection.find_one({"_id": username})
    return user is not None

def addUser(username, password):
    collection.insert_one({"_id": username, "password": password})

def getPassword(username):
    user = collection.find_one({"_id": username})
    return user["password"]

def addFollowing(username, artistID):
    collection.update_one({"_id": username}, {"$addToSet": {"following": artistID}})

def removeFollowing(username, artistID):
    collection.update_one({"_id": username}, {"$pull": {"following": artistID}})

def getAllFollowing(username):
    res = collection.find({"_id": username}, {"_id": 0, "password": 0})
    if not res.alive:
        return []

    doc = res.next()
    return doc["following"]

