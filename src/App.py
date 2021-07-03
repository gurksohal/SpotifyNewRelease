from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from Data import NewReleaseCollection, UserCollection, ArtistCollection
from Spotify import FetchNewReleases, Search

FetchNewReleases.startBackgroundTask()
app = Flask(__name__)
app.config['SECRET_KEY'] = ""
CORS(app)
auth = HTTPBasicAuth()


@app.route("/api/login", methods=["GET"])
def login():
    jsonData = request.authorization
    if jsonData is None or "username" not in jsonData or "password" not in jsonData:
        return jsonify({"success": False})
    if not UserCollection.contains(jsonData["username"]):
        return jsonify({"success": False})
    if not jsonData["username"].isalnum():
        return jsonify({"success": False})

    username = jsonData["username"]
    password = jsonData["password"]
    storedPassword = UserCollection.getPassword(username)
    return jsonify({"success": check_password_hash(storedPassword, password)})


@app.route("/api/new-releases", methods=["GET"])
def newReleases():
    page = request.args.get("page", default=1, type=int)
    search = request.args.get("q", default="")
    if page < 1:
        page = 1
    return jsonify(NewReleaseCollection.read(page, search))


@app.route("/api/user-new-releases", methods=["GET"])
@auth.login_required
def userNewReleases():
    page = request.args.get("page", default=1, type=int)
    search = request.args.get("q", default="")
    if page < 1:
        page = 1
    followingIDs = UserCollection.getAllFollowing(auth.current_user())
    return jsonify(NewReleaseCollection.read(page, search, followingIDs))


@app.route("/api/following", methods=["GET"])
@auth.login_required
def getAllFollowing():
    data = ArtistCollection.getArtist(UserCollection.getAllFollowing(auth.current_user()))
    return jsonify(data)


@app.route("/api/create-user", methods=["POST"])
def createUser():
    jsonData = request.get_json(silent=True, force=True)
    print(request.data)
    if jsonData is None or "username" not in jsonData or "password" not in jsonData:
        return jsonify({"success": False, "reason": "request formatting error"})

    if len(jsonData["username"]) < 3:
        return jsonify({"success": False, "reason": "username should at least be 3 characters"})

    if UserCollection.contains(jsonData["username"]):
        return jsonify({"success": False, "reason": "username already exists"})

    if not jsonData["username"].isalnum():
        return jsonify({"success": False, "reason": "username can only contains letters or numbers"})

    username = jsonData["username"]
    password = generate_password_hash(jsonData["password"])
    UserCollection.addUser(username, password)

    return jsonify({"success": True, "username": username})


@app.route("/api/follow/<artistID>", methods=["PUT"])
@auth.login_required
def followArtist(artistID):
    username = auth.current_user()
    if not ArtistCollection.contains(artistID):
        return jsonify(
            {"success": False, "reason": "artistID:{} not found in database".format(artistID), "username": username})

    UserCollection.addFollowing(username, artistID)
    return jsonify({"success": True, "followed": artistID, "username": username})


@app.route("/api/unfollow/<artistID>", methods=["PUT"])
@auth.login_required
def unfollowArtist(artistID):
    username = auth.current_user()
    UserCollection.removeFollowing(username, artistID)
    return jsonify({"success": True, "un-followed": artistID, "username": username})


@app.route("/api/search-artist/<searchString>", methods=["GET"])
@auth.login_required
def artistSearch(searchString):
    forceSP = request.args.get("force", default=False, type=bool)
    forceSP = True
    if forceSP:
        Search.artistSearch(searchString)

    artists = ArtistCollection.searchArtist(searchString)
    followingArtists = UserCollection.getAllFollowing(auth.current_user())
    returnList = []
    for artist in artists:
        if artist["_id"] not in followingArtists:
            returnList.append(artist)

    return jsonify(returnList)


@auth.verify_password
def verify_password(username, password):
    if not UserCollection.contains(username):
        return False

    storedPassword = UserCollection.getPassword(username)
    return check_password_hash(storedPassword, password)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
