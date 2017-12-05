import numpy as np


class RadiusFrustum:
    """Frustum circulaire/spherique ..."""

    def __init__(self, radius):
        self.agent = None
        self.radius = radius

    def is_in_frustum(self, envObj):
        if np.linalg.norm(envObj.position - self.agent.position) <= self.radius:
            return True
        else:
            return False
