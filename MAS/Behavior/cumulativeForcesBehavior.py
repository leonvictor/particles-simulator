from time import time

import numpy as np
import scipy.constants
import scipy.constants as const

from MAS.influence import *
from MAS.Behavior.forcesComputation import *


class CumulativeForcesBehavior:
    def __init__(self):
        self.agent = None
        self.lastTime = time()
        self.k = 1 / 4 * scipy.constants.pi * scipy.constants.epsilon_0
        self.environment = None

    def act(self, position, perception):

        gravity_forces = ForcesComputation.gravity(self.agent, perception)
        coulomb_forces = ForcesComputation.coulomb(self.agent, perception, self.k)
        vdw_forces = ForcesComputation.vanDerWaals(self.agent, perception)

        # total_acceleration = coulomb_forces + gravity_forces
        total_acceleration = gravity_forces + coulomb_forces + vdw_forces
        total_acceleration = total_acceleration * 10e-17
        #frotements pour le rendu visuel
        total_acceleration -= self.agent.speed / 1.5

        self.agent.acceleration = total_acceleration
        dt = self.environment.deltaTime
        targetPos = self.agent.acceleration*dt*dt + self.agent.speed*dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)
