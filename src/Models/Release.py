class Release:
    def __init__(self, data):
        self.type = data["album_type"]
        self.artists = []
        for artist in data["artists"]:
            a = {"id": artist["id"], "name": artist["name"]}
            self.artists.append(a)

        self.url = data["external_urls"]["spotify"]
        self._id = data["id"]
        self.img = "https://via.placeholder.com/512"
        try:
            self.img = data["images"][0]["url"]
        except:
            pass
        self.name = data["name"]
        self.releaseDate = data["release_date"]
        self.totalTracks = data["total_tracks"]

    def addArtists(self, data):
        ids = set()
        for artist in self.artists:
            ids.add(artist["id"])

        tracks = data["tracks"]["items"]
        for track in tracks:
            for artist in track["artists"]:
                a = {"id": artist["id"], "name": artist["name"]}
                if artist["id"] not in ids:
                    self.artists.append(a)
                    ids.add(artist["id"])

    def getID(self):
        return self._id
