import numpy as np
import scipy.constants as const

import Parameters

class EnvObj:
    """Classe représentant un objet de l'environnement"""

    def __init__(self, environment):
        """self._position = Vector(*((0.0,)*environment.dimension))"""
        """create an array and populate it with random numbers between 0 and 1"""
        self._position = np.random.uniform(-Parameters.BOX_SIZE / 2, Parameters.BOX_SIZE / 2, Parameters.DIMENSION)
        self.gridPos = None
        self.envGrid = None
        self.environment = environment

        self.square = None

        self.mass = 10
        self.charge = 300000
        self.molar_mass = const.Avogadro * self.mass
        self.stiffness = 1

        """following values found on the net, for H2 molecules"""
        # use SI units
        self.dipole_moment = 1 * 3.33564e-30
        self.polarizability = 0.79

    def set_position(self, new_position):
        self._position = new_position
        if self.envGrid:
            self.envGrid.moved(self)

    def get_position(self):
        return self._position

