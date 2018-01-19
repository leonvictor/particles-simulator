from Environment.dataStore import *
from MAS.Behavior.cumulativeForcesBehavior import *
from MAS.Behavior.randomBehavior import *
from MAS.agent import *
from math import ceil, log, sqrt, exp
from Environment.envGrid import *
import numpy as np
import Parameters as param


class Environment:
    """Environment du MAS"""

    DIMENSION = param.DIMENSION
    BOX_SIZE = param.BOX_SIZE

    def __init__(self):
        self.agent_list = []
        self.object_list = []
        self.tree_depth = 0
        self.env_grid = EnvGrid(param.GRID_SIZE)
        self.influence_list = []
        """La permittivité relative dépend du milieu : 1 pour le vide, 1,0006 pour l'air"""
        self.relative_permittivity = 1.0006
        self.last_call_time = time()
        self.data_store = DataStore()
        self.starting_time = self.last_call_time
        self.gas_constant = 8.3144598
        self.sequence = 0
        self.nb_border_collision = 0
        self.friction = 0

    def actualize(self, mass, charge, polarizability, dipole_moment, stiffness, friction):

        self.friction = friction * 1e-2
        for agent in self.agent_list:
            # send updated values to each agent
            agent.update_values(mass=mass,
                                charge=charge,
                                dipole_moment=dipole_moment,
                                polarizability=polarizability,
                                stiffness=stiffness,
                                )
            agent.act()

        length = len(self.influence_list)
        avrSpeed = 0
        self.nb_border_collision = 0
        for i in range(length):
            influence = self.influence_list.pop()
            influence = self.filter_influence(influence)
            self.apply(influence)
            avrSpeed += np.linalg.norm(influence.agent.speed) * influence.agent.molar_mass
        avrSpeed /= length

        self.data_store.temperature[self.sequence] = avrSpeed / (3 * self.gas_constant)

        self.compute_social_entropy()
        self.compute_volume()
        self.compute_pressure()
        self.compute_border_collisions()
        self.compute_partition_function()
        self.sequence += 1

    def get_perception(self, frustum):

        agentPerception = []

        agentListToCheck = []
        maxRank = ceil(frustum.radius / self.env_grid.side)

        agentListToCheck = self.env_grid.get_list_from_rank(frustum.agent.gridPos, maxRank)

        return agentListToCheck

        for obj in agentListToCheck:

            if frustum.is_in_frustum(obj) and frustum.agent != obj:
                agentPerception.append(obj)

        return agentPerception

    def add_influence(self, influence):
        self.influence_list.append(influence)

    def filter_influence(self, influence):
        # for i in self.influence_list:

        if param.BORDER_MODE is param.BorderMode.DONUT:
            out_of_border = False
            position_saved = np.array(influence.position)
            for i in range(0, param.DIMENSION):
                if influence.position[i] > param.BOX_SIZE / 2:
                    out_of_border = True
                    influence.position[i] = -param.BOX_SIZE / 2 + influence.position[i] % (
                            param.BOX_SIZE / 2)
                elif influence.position[i] < -param.BOX_SIZE / 2:
                    out_of_border = True
                    influence.position[i] = param.BOX_SIZE / 2 + influence.position[i] % (
                            -param.BOX_SIZE / 2)
            if out_of_border:
                influence.agent.expected_position = position_saved
            else:
                influence.agent.expected_position = None

        elif param.BORDER_MODE is param.BorderMode.BASIC:
            # clamp influence so that particles remain in the environment
            # we use a random wiggle room to avoid overlapping particles
            rnd = np.random.uniform(0.0001, 0.005)
            influence.position = np.clip(influence.position,
                                         -param.BOX_SIZE / 2 + rnd,
                                         param.BOX_SIZE / 2 - rnd)
        elif param.BORDER_MODE is param.BORDER_MODE.SOLID:
            # we need this loop in case a particle hits multiple borders during one time step
            while not all([-param.BOX_SIZE / 2 < x < param.BOX_SIZE / 2 for x in influence.position]):
                for i in range(0, param.DIMENSION):
                    # if np.linalg.absolute(influence.position[i]) > param.BOX_SIZE/2:
                    #     influence.position[i] = - (influence.position[i]
                    #                                + np.sign(influence.position[i])*param.BOX_SIZE/2
                    #                                - influence.agent.position[i])
                    if influence.position[i] > param.BOX_SIZE / 2:
                        self.nb_border_collision += 1 * influence.agent.kinetic_energy
                        influence.position[i] = - (
                                influence.position[i] - param.BOX_SIZE / 2 - influence.agent.position[i])
                    elif influence.position[i] < -param.BOX_SIZE / 2:
                        self.nb_border_collision += 1 * influence.agent.kinetic_energy
                        influence.position[i] = -(
                                influence.position[i] + param.BOX_SIZE / 2 - influence.agent.position[i])
        return influence

    def apply(self, influence):
        if influence.type == InfluenceType.MOVE:
            influence.agent.position = influence.position

    def add_agent(self, cumulative=True):
        behavior = CumulativeForcesBehavior() if cumulative else RandomBehavior()

        new_agent = Agent(self, RadiusFrustum(param.PERCEPTION_RADIUS), behavior)
        self.agent_list.append(new_agent)
        self.env_grid.add(new_agent)

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

    def compute_volume(self):
        min, max = self.env_grid.get_bounds()
        res = np.empty(param.DIMENSION)
        for i in range(len(min)):
            res[i] = max[i] - min[i]
        volume = 1
        for l in res:
            volume *= l
        self.data_store.volume[self.sequence] = volume

    def compute_pressure(self):
        R = 8.314
        n = len(self.agent_list) / scipy.constants.N_A
        V = self.data_store.volume[self.sequence]
        T = self.data_store.temperature[self.sequence]
        # Pc = 1
        # Tc = 1
        # a = 27*R*R*Tc*Tc/(64*Pc)
        # b = R*Tc/(8*Pc)
        a = 1
        b = 1

        # empirical Waals equation
        P = ((n * R * T) / (V - n * b)) - (n * n * a / V * V)

        self.data_store.pressure[self.sequence] = P

    def compute_social_entropy(self):

        #Moyenne et classes par défaut
        agentListCopy = list(self.agent_list)
        agentListCopy2 = list(self.agent_list)
        class_dict = {}
        index_class = 0
        dist_avg = 0
        cmpt = 0
        dist_min_avg = 0
        while len(agentListCopy) != 0:
            agent = agentListCopy.pop()
            agent.entropy_class = index_class
            class_dict[index_class] = [agent]
            index_class += 1
            minimum = None
            for other in agentListCopy2:
                if other != agent:
                    norm = np.linalg.norm(agent.position - other.position)
                    dist_avg += norm
                    if minimum is None:
                        minimum = norm
                    else:
                        minimum = min(minimum, norm)
                    cmpt += 1
            if minimum is not None:
                dist_min_avg += minimum
        dist_avg /= cmpt
        dist_min_avg /= len(self.agent_list)

        self.data_store.dist_avg[self.sequence] = dist_avg
        self.data_store.dist_min_avg[self.sequence] = dist_min_avg


        #Ecart type
        agentListCopy = list(self.agent_list)
        ecart_type = 0
        cmpt = 0
        ecart_type_min = 0
        while len(agentListCopy) != 0:
            agent = agentListCopy.pop()
            minimum = None
            for other in agentListCopy2:
                if other != agent:
                    cmpt += 1
                    norm = np.linalg.norm(agent.position - other.position)
                    ecart_type += (dist_avg - norm)**2
                    if minimum is None:
                        minimum = norm
                    else:
                        minimum = min(minimum, norm)
            if minimum is not None:
                ecart_type_min += (dist_min_avg - minimum)**2
        ecart_type = sqrt(ecart_type / cmpt)
        ecart_type_min = sqrt(ecart_type_min / len(self.agent_list))
        #self.data_store.dist_standard_deviation_min[self.sequence] = ecart_type_min
        self.data_store.dist_standard_deviation[self.sequence] = ecart_type
        self.data_store.dist_standard_deviation_min[self.sequence] = ecart_type_min


        #Classes pour l'entropie
        agentListCopy = list(self.agent_list)
        while len(agentListCopy) != 0:
            agent = agentListCopy.pop()
            for other in agentListCopy:
                norm = np.linalg.norm(agent.position - other.position)
                if norm < (dist_min_avg + 1 * ecart_type_min) \
                        and agent.entropy_class != other.entropy_class:
                    new = min(agent.entropy_class, other.entropy_class)
                    old = max(agent.entropy_class, other.entropy_class)
                    class_dict[new].extend(class_dict[old])
                    for a in class_dict[old]:
                        a.entropy_class = new
                    del class_dict[old]
        #entropie
        entropy = 0
        for key in class_dict.keys():
            pi = len(class_dict[key])/len(self.agent_list)
            entropy += pi * log(pi)
        entropy = - entropy / log(len(self.agent_list))
        self.data_store.entropy[self.sequence] = entropy

        #Couleur des classes en fonction de la classe
        keylist = class_dict.keys()
        for agent in self.agent_list:
            index = list(keylist).index(agent.entropy_class)
            agent.color = (int(index * 255/len(class_dict)), int(255-index * 255/len(class_dict)), int(255-index * 255/len(class_dict)))

    def compute_border_collisions(self):
        self.data_store.border_collisions[self.sequence] = self.nb_border_collision

    def compute_partition_function(self):
        partition_function = 0
        temperature = self.data_store.temperature[self.sequence]
        thermodynamic_beta = 1/(const.Boltzmann * temperature)
        internal_energy = 0

        for agent in self.agent_list:
            partition_function += exp(-1*(thermodynamic_beta * agent.energy))
            internal_energy += agent.energy

        self.data_store.internal_energy[self.sequence] = internal_energy
        self.data_store.partition_function[self.sequence] = partition_function
        self.data_store.thermodynamic_potential[self.sequence] = -log(partition_function)
        self.data_store.free_energy[self.sequence] = - const.Boltzmann * temperature \
                                                     * log(partition_function)
        enthalpy = internal_energy + self.data_store.pressure[self.sequence]\
                   * self.data_store.volume[self.sequence]
        self.data_store.enthalpy[self.sequence] = enthalpy
        self.data_store.free_enthalpy[self.sequence] = enthalpy - temperature\
                                                       * self.data_store.entropy[self.sequence]

