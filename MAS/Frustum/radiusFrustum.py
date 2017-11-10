from MAS.Frustum.frustum import *

class RadiusFrustum(Frustum):
    """Frustum circulaire/spherique ..."""

    def __init__(self, agent, radius):
        Frustum.__init__(self, agent)
        self.radius = radius

    def is_in_frustum(self, envObj):
        if (envObj.position - self.agent.position).norm() <= self.radius:
            return True
        else:
            return False
