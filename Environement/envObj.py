import numpy as np

class EnvObj:
    """Classe représentant un objet de l'environnement"""

    def __init__(self, environment):
        """self._position = Vector(*((0.0,)*environment.dimension))"""
        """create an array and populate it with random numbers between 0 and 1"""
        self._position = np.random.rand(environment.dimension)
        self.environment = environment
        self.mass = 1
        self.charge = 0


