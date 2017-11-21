from time import time

import numpy as np
import scipy.constants

from MAS.influence import *


class GravityBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()

    def act(self, position, perceptions):
        target_pos = self.agent.position + self.compute_movement_vector(perceptions)
        return Influence(self.agent, InfluenceType.MOVE, position=target_pos)

    def compute_movement_vector(self,perceptions):
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if self in perceptions:
            perceptions.remove(self)
        for p in perceptions:
            """this is necessary for not but shouldn't happen anyway"""
            if p.position.all != self.agent.position.all:
                gravity = scipy.constants.G*((self.agent.mass * p.mass)/(np.linalg.norm(self.agent.position-p.position))**2)
                unit_vector = (self.agent.position-p.position)/np.linalg.norm(self.agent.position-p.position)
                interactions.append(gravity * unit_vector)

        return np.sum(interactions, axis=0)
