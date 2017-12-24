
class DataStore :

    def __init__(self):
        self.temperatureList = {}
        self.entropyList = {}
        self.volume = {}
        self.pression = {}
        self.dist_moy = {}

    def clear(self):
        self.temperatureList.clear()
        self.entropyList.clear()
        self.volume.clear()
        self.pression.clear()
        self.dist_moy.clear()