import numpy as np

class EnvObj:
    """Classe représentant un objet de l'environnement"""

    def __init__(self, environment):
        """self._position = Vector(*((0.0,)*environment.dimension))"""
        """create an array and populate it with random numbers between 0 and 1"""
        self._position = np.random.rand(environment.dimension)
        self.environment = environment

        """we need to copy these values from an actual particle"""
        self.mass = 1
        self.charge = 1

        """following values found on the net, for H2 molecules"""
        self.dipole_moment = 1
        self.polarizability = 0.79


