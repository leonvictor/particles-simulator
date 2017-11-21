from time import time

from MAS.influence import *


class CumulativeForcesBehavior:
    def __init__(self, agent):
        self.agent = agent
        self.lastTime = time()

    def act(self, position, perception):
        gravity_forces = self.agent.gravityBehavior.compute_movement_vector(perception)
        coulomb_forces = self.agent.coulombBehavior.compute_movement_vector(perception)
        vdw_forces = self.agent.vanDerWaalsBehavior.compute_movement_vector(perception)

        total_forces = gravity_forces + coulomb_forces + vdw_forces
        target_pos = self.agent.position + total_forces
        return Influence(self.agent, InfluenceType.MOVE, position=target_pos)

