from time import time

import numpy as np
import scipy.constants
import scipy.constants as const
import Parameters as param

from MAS.influence import *
from MAS.Behavior.forcesComputation import *


class CumulativeForcesBehavior:
    def __init__(self):
        self.agent = None
        self.lastTime = time()
        self.environment = None
        self.friction = 1 #1 means no friction

    def act(self, position, perception):

        gravity_forces = ForcesComputation.gravity(self.agent, perception)
        coulomb_forces = ForcesComputation.coulomb(self.agent, perception)
        vdw_forces = ForcesComputation.vanDerWaals(self.agent, perception)
        spring_forces = ForcesComputation.spring(self.agent, perception)

        # total_acceleration = coulomb_forces + gravity_forces
        # total_acceleration = spring_forces
        total_acceleration = gravity_forces + coulomb_forces + vdw_forces + spring_forces

        total_acceleration = 0

        if param.GRAVITY:
            total_acceleration += gravity_forces
        if param.COULOMB:
            total_acceleration += coulomb_forces
        if param.SPRING:
            total_acceleration += spring_forces
        if param.WAALS:
            total_acceleration += vdw_forces

        # print((np.linalg.norm(gravity_forces), np.linalg.norm(coulomb_forces),
        #        np.linalg.norm(vdw_forces), np.linalg.norm(spring_forces)))
        #frotements
        total_acceleration -= self.agent.speed / self.friction

        self.agent.acceleration = total_acceleration
        self.agent.potiential_energy = np.linalg.norm(total_acceleration)
        dt = param.DELTA_TIME
        targetPos = self.agent.acceleration*dt*dt + self.agent.speed*dt + self.agent.position
        return Influence(self.agent, InfluenceType.MOVE, position=targetPos)
