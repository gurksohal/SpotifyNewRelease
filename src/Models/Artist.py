class Artist:
    def __init__(self, data):
        self._id = data["id"]
        self.img = "https://via.placeholder.com/512"
        try:
            self.img = data["images"][0]["url"]
        except:
            pass
        self.name = data["name"]
        self.popularity = data["popularity"]