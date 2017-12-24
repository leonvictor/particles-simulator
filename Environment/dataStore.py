
class DataStore :

    def __init__(self):

        self.temperatureList = {}
        self.entropyList = {}
        self.volume = {}
        self.pression = {}
        self.border_collisions = {}

    def clear(self):
        self.temperatureList.clear()
        self.entropyList.clear()
        self.volume.clear()
        self.pression.clear()
        self.border_collisions.clear()
