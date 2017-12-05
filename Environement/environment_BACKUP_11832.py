from Environement.dataStore import *
from MAS.Behavior.randomBehavior import *
from MAS.agent import *
from Others.envGrid import  *
from math import  ceil

class Environment:
    """Environment du MAS"""

    def __init__(self, dim):
        self.dimension = dim
        self.agentList = []
        self.objectList = []
        self.treeDepth = 0
        self.envGrid = EnvGrid(30)
        self.influenceList = []
        """La permittivité relative dépend du milieu : 1 pour le vide, 1,0006 pour l'air"""
        self.relative_permittivity = 1.0006
        # mise à jour du temps
        self.deltaTime = 0.01
        self.lastCallTime = time()
        self.dataStore = DataStore()
        self.startingTime = self.lastCallTime
        self.gasConstant = 8.3144598

    def actualize(self, mass, charge):
        for agent in self.agentList:
            # send updated values to each agent
            agent.update_values(mass=mass, charge=charge)

            agent.act()

        length = len(self.influenceList)

        avrSpeed = np.zeros(self.dimension)

        now = time()
        self.deltaTime = now - self.lastCallTime
        self.lastCallTime = now

        for i in range(length):
            influence = self.influenceList.pop()
            influence = self.checkInfluence(influence)
            self.apply(influence)
            avrSpeed += np.linalg.norm(influence.agent.speed)

        avrSpeed /= length
        self.dataStore.speedList[now - self.startingTime] = avrSpeed * agent.molar_mass / (3 * self.gasConstant)

    def getPerception(self, frustum):

        agentPerception = []

        agentListToCheck = []
        maxRank = ceil(frustum.radius/self.envGrid.side)

        agentListToCheck = self.envGrid.getListFromRank(frustum.agent.gridPos, maxRank)


        for obj in agentListToCheck:

<<<<<<< HEAD
            if frustum.is_in_frustum(obj) and frustum.agent != obj:
=======
            elif frustum.is_in_frustum(obj) and frustum.agent != obj:
>>>>>>> 7d37877ed506ffea0383ae7c80f1a919e27a44d6
                agentPerception.append(obj)

        return agentPerception

    def addInfluence(self, influence):
        self.influenceList.append(influence)

    def checkInfluence(self, influence):
        # TODO

        return influence

    def apply(self, influence):
        if influence.type == InfluenceType.MOVE:
            influence.agent.position = influence.position

    def addAgent(self):
        new_agent = Agent(self, RadiusFrustum(100), RandomBehavior())
        self.agentList.append(new_agent)
<<<<<<< HEAD
        self.envGrid.add(new_agent)

=======
        self.quadTree.add(new_agent)
>>>>>>> 7d37877ed506ffea0383ae7c80f1a919e27a44d6
