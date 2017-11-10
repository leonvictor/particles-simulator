from enum import Enum


class InfluenceType(Enum):
    MOVE = 1


class Influence:

    def __init__(self, agent, type, **kwargs):
        self.agent = agent
        self.type = type

        if type == InfluenceType.MOVE:
            self.position = kwargs["position"]


