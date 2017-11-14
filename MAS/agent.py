from Environement.envObj import *
from MAS.Behavior.gravityBehavior import GravityBehavior
from Others.vector import *
from MAS.Frustum.radiusFrustum import *
from time import time


class Agent(EnvObj):

    def __init__(self, environment, frustumType, behavior = None):
        EnvObj.__init__(self, environment)
        """Temporary initialization for testing purpose"""
        self.gravityBehavior = GravityBehavior()
        self.behavior = behavior
        self.behavior.agent = self
        self.speed = Vector(*((0.0,)*environment.dimension))
        self.acceleration = Vector(*((0.0,)*environment.dimension))
        self.deltaTime = 0.01
        self.lastCallTime = time()
        self.lastPosition = self._position

        if frustumType == FrustumType.RadiusFrustum:
            self.frustum = RadiusFrustum(self, 5)
        print("agent créé")



    def act(self):
        if self.behavior is not None:
            perceptions = self.environment.getPerception(self.frustum)
            if not perceptions:
                influence = self.behavior.act(self.position, perceptions)
            else:
                influence = self.gravityBehavior.act(self.position, perceptions)
            influence.agent = self
            self.environment.addInfluence(influence)

    def moved(self):
        """"Update speed and deltaTime"""
        now = time()
        self.deltaTime = now - self.lastCallTime
        self.lastCallTime = now
        self.speed = (self.position - self.lastPosition)

        self.speed = self.speed / self.deltaTime
        self.lastPosition = self.position
        print("agent moved to {0}".format(self.position))

    def _set_position(self, new_position):
        self._position = new_position
        self.moved()

    def _get_position(self):
        return self._position

    position = property(_get_position, _set_position)