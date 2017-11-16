from time import time

import numpy as np
import scipy as sp

from MAS.influence import *


class coulombBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()

    def act(self, position, perception):
        acceleration = []
        interactions = []
        for p in perception:
            k = 1/4*sp.constant.pi*sp.constant.epsilon_0
            interactions.append(k*(np.absolute(self.agent.charge*p.charge)/(np.linalg.norm(self.agent.position-p.position))**2))*(self.agent.position-p.position)*np.linalg(self.agent.position-p.position)

        """We need to make sure the mean force is calculated along the right axis"""
        meanforce = np.mean(interactions)

        """Not sure how to compute the target pos for now"""
        targetPos = self.agent.position + meanforce
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)
