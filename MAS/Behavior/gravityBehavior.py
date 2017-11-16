from time import time

import numpy as np
import scipy.constants

from MAS.influence import *


class GravityBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()

    def act(self, position, perception):
        acceleration = []
        interactions = []
        """It's ok to perceive yourself, but not to be attracted by yourself"""
        if self in perception:
            perception.remove(self)
        for p in perception:
            """this is necessary for not but shouldn't happen anyway"""
            if p.position.all != self.agent.position.all:
                interactions.append((scipy.constants.G*((self.agent.mass * p.mass)/(np.linalg.norm(self.agent.position-p.position))**2))*(self.agent.position-p.position)/np.linalg.norm(self.agent.position-p.position))

        meanforce = np.mean(interactions)

        """Not sure how to compute the target pos for now"""
        targetPos = self.agent.position + meanforce
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)
