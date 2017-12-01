from MAS.Behavior.randomBehavior import *
from MAS.Frustum.frustum import *
from MAS.agent import *
from Others.quadTree import *
from Environement.dataStore import *


class Environment :
    """Environment du MAS"""

    def __init__(self, dim):
        self.dimension = dim
        self.agentList = []
        self.objectList = []
        self.treeDepth = 0
        self.quadTree = QuadTree(dim, self.treeDepth)
        self.influenceList = []
        """La permittivité relative dépend du milieu : 1 pour le vide, 1,0006 pour l'air"""
        self.relative_permittivity = 1.0006
        #mise à jour du temps
        self.deltaTime = 0.01
        self.lastCallTime = time()
        self.episode = 0.0
        self.dataStore = DataStore()


    def actualize(self):
        for agent in self.agentList:
            agent.act()

        length = len(self.influenceList)

        avrSpeed = Vector(*((0.0,)*self.dimension))

        now = time()
        self.deltaTime = now - self.lastCallTime
        self.lastCallTime = now

        for i in range(length):
            influence = self.influenceList.pop()
            influence = self.checkInfluence(influence)
            self.apply(influence)
            avrSpeed += influence.agent.speed

        avrSpeed /= length
        self.dataStore.speedList[self.episode] = avrSpeed
        self.episode += 1



    def getPerception(self, frustum):

        agentPerception = []

        # return agentPerception

        nodesToExplore = [list(self.quadTree.nodes)]

        for obj in nodesToExplore.pop():

            if obj is QuadTree:
                # TODO : control node before adding
                nodesToExplore.append(obj)

            elif frustum.is_in_frustum(obj):
                    agentPerception.append(obj)

        return agentPerception

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

