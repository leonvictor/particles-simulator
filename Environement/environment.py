from Environement.dataStore import *
from MAS.Behavior.randomBehavior import *
from MAS.agent import *
from Environement.envGrid import  *
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
        self.deltaTime = 0.1
        self.lastCallTime = time()
        self.dataStore = DataStore()
        self.startingTime = self.lastCallTime
        self.gasConstant = 8.3144598
        self.sequence = 0

    def actualize(self, mass, charge, polarizability, dipole_moment):
        for agent in self.agentList:
            # send updated values to each agent
            agent.update_values(mass=mass,
                                charge=charge,
                                polarizability=polarizability,
                                dipole_moment=dipole_moment)

            agent.act()

        length = len(self.influenceList)

        avrSpeed = np.zeros(self.dimension)

        for i in range(length):
            influence = self.influenceList.pop()
            influence = self.checkInfluence(influence)
            self.apply(influence)
            avrSpeed += np.linalg.norm(influence.agent.speed)

        avrSpeed /= length
        self.dataStore.speedList[self.sequence] = avrSpeed * agent.molar_mass \
                                                  / (3 * self.gasConstant)

        self.envGrid.save(str(mass) + "_" + str(charge) + "_" + str(polarizability) +
                          "_" + str(dipole_moment) + "_" + str(self.sequence) + "_")
        self.sequence += 1

    def getPerception(self, frustum):

        agentPerception = []

        agentListToCheck = []
        maxRank = ceil(frustum.radius/self.envGrid.side)

        agentListToCheck = self.envGrid.getListFromRank(frustum.agent.gridPos, maxRank)


        return agentListToCheck

        for obj in agentListToCheck:

            if frustum.is_in_frustum(obj) and frustum.agent != obj:

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
        new_agent = Agent(self, RadiusFrustum(500), RandomBehavior())
        self.agentList.append(new_agent)
        self.envGrid.add(new_agent)

