
class DataStore :

    def __init__(self):
        self.temperature = {}
        self.entropy = {}
        self.volume = {}
        self.pressure = {}
        self.dist_moy = {}
        self.border_collisions = {}
        self.partition_function = {}

    def clear(self):
        self.temperature.clear()
        self.entropy.clear()
        self.volume.clear()
        self.pressure.clear()
        self.dist_moy.clear()
        self.border_collisions.clear()
        self.partition_function.clear()
