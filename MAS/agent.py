from Environment.envObj import *
from MAS.Frustum.radiusFrustum import *
import Parameters as param
from scipy import constants as const


class Agent(EnvObj):

    def __init__(self, environment, frustum, behavior = None):
        EnvObj.__init__(self, environment)
        """Temporary initialization for testing purpose"""

        self.behavior = behavior
        self.init_behavior(behavior)
        self.speed = np.zeros(param.DIMENSIONS)
        self.acceleration = np.zeros(param.DIMENSIONS)

        self.last_position = self.position
        self.expected_position = None

        self.frustum = frustum
        self.frustum.agent = self
        self.entropy_class = None
        self.kinetic_energy = 0
        self.color = (0, 0, 0)
        self.potiential_energy = 0
        #print("agent créé")

    def init_behavior(self, behavior):
        behavior.agent = self
        behavior.environment = self.environment

    def act(self):
        if self.behavior is not None:
            perceptions = self.environment.get_perception(self.frustum)
            if not perceptions or len(perceptions) <= 1:
                influence = self.behavior.act(self.position, perceptions)
            else:
                influence = self.behavior.act(self.position, perceptions)
            influence.agent = self
            self.environment.add_influence(influence)

    def moved(self):
        """"Update speed and delta_time"""
        if self.expected_position is None:
            self.expected_position = self.position
        self.speed = (self.expected_position - self.last_position)
        self.speed /= param.DELTA_TIME
        self.kinetic_energy = 0.5 * self.mass * (np.linalg.norm(self.speed) ** 2)
        self.last_position = self.position
        self.expected_position = None
        #print("agent moved to {0}".format(self.position))

    def _set_position(self, new_position):
        EnvObj.set_position(self, new_position)
        self.moved()

    def _get_position(self):
        return EnvObj.get_position(self)

    def _set_mass(self, new_mass):
        # for realistic values
        # self._mass = const.pico * new_mass
        self._mass = new_mass
        self.molar_mass = new_mass * const.Avogadro

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

    def _get_energy(self):
        return self.potiential_energy + self.kinetic_energy

    position = property(_get_position, _set_position)
    mass = property(_get_mass, _set_mass)
    charge = property(_get_charge, _set_charge)
    polarizability = property(_get_polarizability, _set_polarizability)
    dipole_moment = property(_get_dipole_moment, _set_dipole_moment)
    stiffness = property(_get_stiffness, _set_stiffness)
    energy = property(_get_energy)
