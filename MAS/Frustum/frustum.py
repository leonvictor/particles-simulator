from enum import Enum


class FrustumType(Enum):
    RadiusFrustum = 1000000


class Frustum:
    """Classe abstraite pour frustum"""

    def __init__(self, agent):
        self.agent = agent

    def is_in_frustum(self, envObj):
        raise NotImplementedError
