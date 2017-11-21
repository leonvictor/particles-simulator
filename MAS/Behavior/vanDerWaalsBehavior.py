from time import time

import numpy as np
import scipy.constants as const

from MAS.influence import *


class VanDerWaalsBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()

    def act(self, position, perceptions):


        """Not sure how to compute the target pos for now"""
        target_vector = self.compute_movement_vector(perceptions)
        target_pos = self.agent.position + target_vector
        # target_pos = self.agent.position + self.compute_movement_vector(perceptions)
        return Influence(self.agent, InfluenceType.MOVE, position=target_pos)

    def compute_movement_vector(self, perceptions):
        interactions = []
        if self in perceptions:
            perceptions.remove(self)
        for p in perceptions:
            if p.position.all != self.agent.position.all:
                """absolute temperature = 0K or -273.15°C or -459.67°F"""
                absolute_temperature = -273.15
                e_keesom = ((self.agent.dipole_moment ** 2)*(p.dipole_moment ** 2))/(3 *((4*const.pi*const.epsilon_0 * self.agent.environment.relative_permittivity) ** 2) * const.k * absolute_temperature)
                e_debye = (((self.agent.dipole_moment ** 2) * p.polarizability) + ((p.dipole_moment ** 2)*self.agent.polarizability))/(4 * const.pi * const.epsilon_0 * self.agent.environment.relative_permittivity)

                electronic_absorption_frequency = 10
                """ICI : Pas encore trouvé ce que c'est vraiment"""

                e_london = (
                           const.Planck * electronic_absorption_frequency * self.agent.polarizability * p.polarizability) / (
                           4 * const.pi * const.epsilon_0 * self.agent.environment.relative_permittivity)
                vdw = (- 1 / (np.linalg.norm(self.agent.position - p.position) ** 6)) * (e_keesom + e_debye + e_london)

                unit_vector = (self.agent.position - p.position) / np.linalg.norm(self.agent.position - p.position)
                interactions.append(vdw * unit_vector)
        return np.sum(interactions,axis=0)

