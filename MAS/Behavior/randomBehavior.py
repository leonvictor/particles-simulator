from random import uniform
import numpy as np

import Parameters as param
from MAS.influence import *


class RandomBehavior:

    def __init__(self):
        self.agent = None
        self.environment = None

    def act(self, perception):

        old = self.agent.acceleration
        self.agent.acceleration = np.zeros(self.environment.DIMENSION)

        self.agent.acceleration = np.random.rand(self.environment.DIMENSION)
        # print(self.agent.acceleration)
        self.agent.acceleration = self.agent.acceleration - 0.5
        self.agent.acceleration *= param.RANDOM_ACC_FACTOR
        self.agent.acceleration += 0.3*old

        self.agent.acceleration -= self.environment.friction * self.agent.speed

        dt = param.DELTA_TIME
        targetPos = self.agent.acceleration*dt*dt + self.agent.speed*dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)
