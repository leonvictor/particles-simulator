from random import uniform

import numpy as np

from MAS.influence import *


class RandomBehavior:

    def __init__(self):
        self.agent = None
        self.environment = None

    def act(self):
        self.agent.acceleration = (np.random.rand(self.environment.dimension) - 0.5) * 5
        dt = self.environment.deltaTime
        target_pos = self.agent.acceleration*dt*dt + self.agent.speed*dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position=target_pos)

