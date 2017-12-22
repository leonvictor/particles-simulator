from time import time

from Environement.envObj import *
from MAS.Behavior.cumulativeForcesBehavior import CumulativeForcesBehavior
from MAS.Frustum.radiusFrustum import *
from scipy import constants as const


class Agent(EnvObj):

    def __init__(self, environment, frustum, behavior = None):
        EnvObj.__init__(self, environment)
        """Temporary initialization for testing purpose"""

        self.behavior = behavior
        self.initBehavior(behavior)
        self.speed = np.zeros(self.environment.dimension)
        self.acceleration = np.zeros(self.environment.dimension)

        self.lastPosition = self.position
        self.expectedPosition = None

        self.frustum = frustum
        self.frustum.agent = self

        #print("agent créé")

    def initBehavior(self, behavior):
        behavior.agent = self
        behavior.environment = self.environment

    def act(self):
        if self.behavior is not None:
            perceptions = self.environment.getPerception(self.frustum)
            if not perceptions or len(perceptions) <= 1:
                influence = self.behavior.act(self.position, perceptions)
            else:
                influence = self.behavior.act(self.position, perceptions)
            influence.agent = self
            self.environment.addInfluence(influence)

    def moved(self):
        """"Update speed and deltaTime"""
        if self.expectedPosition is None:
            self.expectedPosition = self.position
        self.speed = (self.expectedPosition - self.lastPosition)
        self.speed /= self.environment.deltaTime
        self.lastPosition = self.position
        #print("agent moved to {0}".format(self.position))

    def _set_position(self, new_position):
        EnvObj.set_position(self, new_position)
        self.moved()

    def _get_position(self):
        return EnvObj.get_position(self)

    def _set_mass(self, new_mass):
        # for realistic values
        # self._mass = const.pico * new_mass
        self._mass = new_mass * 1e4
        self.molar_mass = new_mass * 1e4 * const.Avogadro

    def _get_mass(self):
        return self._mass

    def _set_charge(self, new_charge):
        self._charge = new_charge * 1e4

    def _get_charge(self):
        return self._charge

    def _set_polarizability(self, new_polarizability):
        self._polarizability = new_polarizability

    def _get_polarizability(self):
        return self._polarizability

    def _set_dipole_moment(self, new_dipole_moment):
        self._dipole_moment = new_dipole_moment

    def _get_dipole_moment(self):
        return self._dipole_moment

    def _get_stiffness(self):
        return self._stiffness

    def _set_stiffness(self, stiffness):
        self._stiffness = stiffness

    def update_values(self, mass, charge, polarizability, dipole_moment, stiffness):
        # print("my new mass is", mass)
        self.mass = mass
        self.charge = charge
        self.dipole_moment = dipole_moment
        self.polarizability = polarizability
        self.stiffness = stiffness

    position = property(_get_position, _set_position)
    mass = property(_get_mass, _set_mass)
    charge = property(_get_charge, _set_charge)
    polarizability = property(_get_polarizability, _set_polarizability)
    dipole_moment = property(_get_dipole_moment, _set_dipole_moment)
    stiffness = property(_get_stiffness, _set_stiffness)
