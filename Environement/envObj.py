import numpy as np
import scipy.constants as const


class EnvObj:
    """Classe représentant un objet de l'environnement"""

    def __init__(self, environment):
        """self._position = Vector(*((0.0,)*environment.dimension))"""
        """create an array and populate it with random numbers between 0 and 1"""
        self._position = np.random.uniform(0.5, 200, environment.dimension)
        self.environment = environment

        """we need to copy these values from an actual particle"""
        self.mass = 10
        self.charge = 300000
        self.molarMass = const.Avogadro * self.mass

        """following values found on the net, for H2 molecules"""
        # use SI units
        self.dipole_moment = 1 * 3.33564e-30
        self.polarizability = 0.79


