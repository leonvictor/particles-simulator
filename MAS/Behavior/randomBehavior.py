from random import uniform
from time import time

from MAS.influence import *
from Others.vector import *


class RandomBehavior:

    def __init__(self):
        self.agent = None
        self.lastTime = time()

    def act(self, position, perception):

        acceleration = []
        for i in range(len(self.agent.acceleration)):
            acceleration.append(uniform(-100, 100)+self.agent.acceleration[i]/10000)

        self.agent.acceleration = Vector(*tuple(acceleration))
        dt = self.agent.deltaTime
        targetPos = self.agent.acceleration*dt*dt + self.agent.speed*dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position = targetPos)

