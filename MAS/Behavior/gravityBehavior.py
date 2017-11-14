import numpy as np
import scipy as sp

from MAS.influence import *
from random import uniform
from Others.vector import *
from time import time


class GravityBehavior:
    def __init__(self):
        self.agent = None
        self.lastTime = time()

    def act(self, position, perception):
        acceleration = []
        interactions = []
        for p in perception:
            interactions.append(sp.constants.G*(self.mass * p.mass)/np.linalg.norm(self.position-p.position))

        """We need to make sure the mean force is calculated along the right axis"""
        meanforce = np.mean(interactions)

        """Not sure how to compute the target pos for now"""
        targetPos = self.agent.position + meanforce
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)

        """We still use a random behavior while this is not functional"""
        """for i in range(len(self.agent.acceleration)):
            acceleration.append(uniform(-0.01, 0.01) + self.agent.acceleration[i] / 100)

        self.agent.acceleration = Vector(*tuple(acceleration))
        dt = self.agent.deltaTime
        targetPos = self.agent.acceleration * dt * dt + self.agent.speed * dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)"""
