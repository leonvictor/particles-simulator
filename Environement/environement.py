from Others.quadTree import *
from MAS.agent import *
from MAS.Frustum.frustum import *
from MAS.influence import *
from MAS.Behavior.randomBehavior import *

class Environement :
    """Environement du MAS"""

    def __init__(self, dim):
        self.dimension = dim
        self.agentList = []
        self.objectList = []
        self.treeDepth = 0
        self.quadTree = QuadTree(dim, self.treeDepth)
        self.influenceList = []

    def actualize(self):
        for agent in self.agentList:
            agent.act()

        length = len(self.influenceList)
        for i in range(length):
            influence = self.influenceList.pop()
            influence = self.checkInfluence(influence)
            self.apply(influence)

    def getPerception(self, frustum):

        agentPerception = []
        nodesToExplore = [list(self.quadTree.nodes)]

        for obj in nodesToExplore.pop():

            if obj is QuadTree:
                # TODO : control node before adding
                nodesToExplore.append(obj)

            elif frustum.is_in_frustum(obj):
                    agentPerception.append(obj)

    def addInfluence(self, influence):
        self.influenceList.append(influence)

    def checkInfluence(self, influence):
        # TODO

        return influence

    def apply(self, influence):
        if influence.type == InfluenceType.MOVE :
            influence.agent.position = influence.position

    def addAgent(self):
        new_agent = Agent(self, FrustumType.RadiusFrustum, RandomBehavior())
        self.agentList.append(new_agent)
        self.quadTree.add(new_agent)

