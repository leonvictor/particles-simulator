from Environement.dataStore import *
from MAS.Behavior.cumulativeForcesBehavior import *
from MAS.agent import *
from Environement.envGrid import *
from math import ceil
from math import log
import numpy as np
import Parameters as param


class Environment:
    """Environment du MAS"""

    DIMENSION = 2
    BOX_SIZE = 600

    def __init__(self):
        self.dimension = Environment.DIMENSION
        self.agentList = []
        self.objectList = []
        self.treeDepth = 0
        self.envGrid = EnvGrid(100)
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
                                dipole_moment=dipole_moment,
                                polarizability=polarizability)
            agent.act()

        length = len(self.influenceList)
        avrSpeed = np.zeros(self.dimension)
        for i in range(length):
            influence = self.influenceList.pop()
            influence = self.filterInfluence(influence)
            self.apply(influence)
            avrSpeed += np.linalg.norm(influence.agent.speed) * influence.agent.molar_mass
        avrSpeed /= length

        self.dataStore.temperatureList[self.sequence] = avrSpeed / (3 * self.gasConstant)

        name = (str(mass) + "_" + str(charge) + "_" + str(polarizability) +
                "_" + str(dipole_moment) + "_" + str(self.sequence) + "_")
        self.envGrid.save(name)
        self.compute_entropy(name)
        self.sequence += 1

    def getPerception(self, frustum):

        agentPerception = []

        agentListToCheck = []
        maxRank = ceil(frustum.radius / self.envGrid.side)

        agentListToCheck = self.envGrid.getListFromRank(frustum.agent.gridPos, maxRank)

        return agentListToCheck

        for obj in agentListToCheck:

            if frustum.is_in_frustum(obj) and frustum.agent != obj:
                agentPerception.append(obj)

        return agentPerception

    def addInfluence(self, influence):
        self.influenceList.append(influence)

    def filterInfluence(self, influence):
        # for i in self.influenceList:

        if param.BORDER_MODE is param.BorderMode.DONUT:
            out_of_boarder = False
            position_saved = np.array(influence.position)
            for i in range(0, Environment.DIMENSION):
                if influence.position[i] > Environment.BOX_SIZE/2:
                    out_of_boarder = True
                    influence.position[i] = -Environment.BOX_SIZE/2 + influence.position[i] % (Environment.BOX_SIZE / 2)
                elif influence.position[i] < -Environment.BOX_SIZE/2:
                    out_of_boarder = True
                    influence.position[i] = Environment.BOX_SIZE/2 + influence.position[i] % (-Environment.BOX_SIZE / 2)
            if(out_of_boarder):
                influence.agent.expectedPosition = position_saved
            else:
                influence.agent.expectedPosition = None

        elif param.BORDER_MODE is param.BorderMode.SOLID:
            # clamp influence so that particles remain in the environment
            # we use a random wiggle room to avoid overlapping particles
            rnd = np.random.uniform(0.0001, 0.005)
            influence.position = np.clip(influence.position,
                                         -Environment.BOX_SIZE / 2 + rnd,
                                         Environment.BOX_SIZE / 2 - rnd)

        # influence.position[0] = max(min(Environment.BOX_SIZE / 2, influence.position[0]), -Environment.BOX_SIZE / 2)
        # influence.position[1] = max(min(Environment.BOX_SIZE / 2, influence.position[1]), -Environment.BOX_SIZE / 2)
        return influence

    def apply(self, influence):
        if influence.type == InfluenceType.MOVE:
            influence.agent.position = influence.position

    def addAgent(self):
        new_agent = Agent(self, RadiusFrustum(500), CumulativeForcesBehavior())
        self.agentList.append(new_agent)
        self.envGrid.add(new_agent)

    @staticmethod
    def get_probability_grid_all(ranges_list_input, max_sequence):
        """Récupère les dictionnaires grille/nb_agent_moyen pour toutes les configurations possibles,
        l'input doit impératvement être des ranges et dans l'ordre de l'utilisation dans le nommage des fichiers"""

        # on construit une liste avec toutes les configurations possibles déterminées à partir des ranges en input
        # chaque configuration contient les valeurs de paramètres
        configurations = Environment.build_list(ranges_list_input)
        result = {}
        for configuration in configurations:
            name = ""
            for i in configuration:
                name += str(i) + "_"
            result[configuration] = Environment.get_probability_grid_name(name, max_sequence)
        return result

    @staticmethod
    def get_probability_grid_config(mass, charge, polarizability, dipole_moment, max_sequence):
        l = (mass, charge, polarizability, dipole_moment)
        name = ""
        for i in l:
            name += str(i) + "_"
        result = Environment.get_probability_grid_name(name, max_sequence)

        if len(result[max_sequence - 1]) == 0:
            return None

        return result

    @staticmethod
    def get_probability_grid_name(name, max_sequence):
        """Récupère le dictionnaire grille/probabilité pour toutes les séquences d'une configuration de paramètres"""
        result = {}
        for i in range(0, max_sequence):
            name_seq = name + str(i) + "_"
            result[i] = Environment.get_probability_grid_name_sequence(name_seq)
        return result

    @staticmethod
    def get_probability_grid_name_sequence(name):
        """Récupère le dicitionnaire grille/probabilité dans tous les fichiers correspondants"""
        result = {}

        files = []

        os.makedirs(EnvGrid.path, exist_ok=True)

        for f in os.listdir(EnvGrid.path):
            if f.startswith(name):
                files.append(f)

        for filename in files:
            file = EnvGrid.load(filename)
            nb_agent = 0
            for v in file.values():
                nb_agent += v

            for k, v in file.items():
                if k in result.keys():
                    result[k] += v / nb_agent
                else:
                    result[k] = v / nb_agent

        for key in result.keys():
            result[key] /= len(files)
        return result

    @staticmethod
    def build_list(range_array):
        return Environment._build_list(range_array, np.zeros(len(range_array)), 0)

    @staticmethod
    def _build_list(range_array, array_in, index):
        result = []

        for i in range_array[index]:
            tab = list(array_in)
            tab[index] = i
            if index + 1 < len(range_array):
                result.extend(Environment._build_list(range_array, tab, index + 1))
            else:
                result.append(tuple(tab))

        return result

    def compute_entropy(self, name):
        entropy = 0
        data = Environment.get_probability_grid_name_sequence(name)

        for pi in data.values():
            entropy += pi * log(pi)
        entropy = - entropy / log(len(data))

        self.dataStore.entropyList[self.sequence] = entropy
