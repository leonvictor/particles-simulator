from time import time

import numpy as np
import scipy.constants

from MAS.influence import *


class CoulombBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()
        self.k = 1/4*scipy.constants.pi*scipy.constants.epsilon_0


    def act(self, position, perception):
        target_pos = self.agent.position + self.compute_movement_vector(perception)
        return Influence(self.agent, InfluenceType.MOVE, position=target_pos)

    def compute_movement_vector(self, perception):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if self in perception:
            perception.remove(self)
        for p in perception:
            """this is necessary for now but shouldn't happen anyway"""
            if p.position.all != self.agent.position.all:
                coulomb = self.k * np.absolute(self.agent.charge * p.charge) / (np.linalg.norm(p.position - self.agent.position) ** 2)
                #repulsive force : the vector is away from p
                unit_vector = (p.position - self.agent.position) * np.linalg.norm(p.position - self.agent.position)
                interactions.append(coulomb * unit_vector)


        return np.sum(interactions, axis=0)

