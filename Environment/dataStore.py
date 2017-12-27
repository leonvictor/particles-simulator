
class DataStore :

    def __init__(self):
        self.temperature_list = {}
        self.entropy_list = {}
        self.volume = {}
        self.pression = {}
        self.dist_moy = {}
        self.border_collisions = {}

    def clear(self):
        self.temperature_list.clear()
        self.entropy_list.clear()
        self.volume.clear()
        self.pression.clear()
        self.dist_moy.clear()
        self.border_collisions.clear()
