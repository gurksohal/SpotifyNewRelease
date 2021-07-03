import threading
import datetime

from Spotify.API import sp
from Data import NewReleaseCollection
from Models.Release import Release


def fetchNewReleases(offset):
    results = sp.new_releases("CA", 50, offset)
    newReleases = []
    releaseObjects = []
    releaseDict = {}
    for data in results["albums"]["items"]:
        try:
            releaseObject = Release(data)
            releaseObjects.append(releaseObject)
            releaseDict[releaseObject.getID()] = releaseObject
        except KeyError or TypeError:
            log("Unable to create Release object.")

    loadAllArtists(releaseObjects, releaseDict)

    for releaseObject in releaseObjects:
        newReleases.append(releaseObject.__dict__)

    # if we can write all of them, fetch another 50
    if NewReleaseCollection.write(newReleases):
        log("offset={}, nextOffSet={}, fetching more".format(offset, offset + 50))
        fetchNewReleases(offset + 50)
    else:
        log("offset={}, done fetching songs".format(offset))


def loadAllArtists(listOfReleases, releaseDict):
    idLists = breakListIntoSize(listOfReleases)
    results = []
    for idList in idLists:
        tempDict = sp.albums(idList)
        albums = tempDict["albums"]
        for album in albums:
            results.append(album)

    for albumData in results:
        releaseObject = releaseDict[albumData["id"]]
        releaseObject.addArtists(albumData)


def breakListIntoSize(listOfReleases):
    returnList = []
    currList = []
    for release in listOfReleases:
        currList.append(release.getID())
        if len(currList) == 20:
            returnList.append(currList)
            currList = list()

    if len(currList) > 0:
        returnList.append(currList)

    return returnList


def startBackgroundTask():
    log("Start fetching")
    threading.Timer(60 * 15, startBackgroundTask).start()
    fetchNewReleases(0)


def log(msg):
    print("[{}] {}".format(datetime.datetime.now(), msg))
