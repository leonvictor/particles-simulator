from time import time

from Environement.envObj import *
from MAS.Behavior.cumulativeForcesBehavior import CumulativeForcesBehavior
from MAS.Frustum.radiusFrustum import *


class Agent(EnvObj):

    def __init__(self, environment, frustumType, behavior = None):
        EnvObj.__init__(self, environment)
        """Temporary initialization for testing purpose"""

        self.cumulativeForcesBehavior = CumulativeForcesBehavior()
        self.behavior = behavior
        self.initBehavior(behavior)
        self.initBehavior(self.cumulativeForcesBehavior)
        self.speed = np.zeros(self.environment.dimension)
        self.acceleration = np.zeros(self.environment.dimension)

        self.lastPosition = self.position

        if frustumType == FrustumType.RadiusFrustum:
            self.frustum = RadiusFrustum(self, 100)
        #print("agent créé")

    def initBehavior(self, behavior):
        behavior.agent = self
        behavior.environment = self.environment

    def act(self):
        if self.behavior is not None:
            perceptions = self.environment.getPerception(self.frustum)
            if not perceptions or len(perceptions) <= 1:
                influence = self.behavior.act(self.position, perceptions)
            else:
                #influence = self.behavior.act(self.position, perceptions)
                influence = self.cumulativeForcesBehavior.act(self.position, perceptions)
            influence.agent = self
            self.environment.addInfluence(influence)

    def moved(self):
        """"Update speed and deltaTime"""

        self.speed = (self.position - self.lastPosition)

        self.speed = self.speed / self.environment.deltaTime
        self.lastPosition = self.position
        #print("agent moved to {0}".format(self.position))

    def _set_position(self, new_position):
        self._position = new_position
        self.moved()

    def _get_position(self):
        return self._position

    position = property(_get_position, _set_position)