import Parameters as param


class DataStore:

    def __init__(self):
        self.temperature = {}
        self.entropy = {}
        self.volume = {}
        self.pressure = {}
        self.dist_avg = {}
        self.border_collisions = {}
        self.partition_function = {}
        self.thermodynamic_potential = {}
        self.free_energy = {}
        self.dist_min_avg = {}
        self.internal_energy = {}
        self.enthalpy = {}
        self.free_enthalpy = {}
        self.dist_standard_deviation = {}
        self.dist_standard_deviation2 = {}

    def clear(self):
        self.temperature.clear()
        self.entropy.clear()
        self.volume.clear()
        self.pressure.clear()
        self.dist_avg.clear()
        self.border_collisions.clear()
        self.partition_function.clear()
        self.thermodynamic_potential.clear()
        self.free_energy.clear()
        self.dist_min_avg.clear()
        self.internal_energy.clear()
        self.enthalpy.clear()
        self.free_enthalpy.clear()
        self.dist_standard_deviation.clear()
        self.dist_standard_deviation2.clear()

    def _get_border_collision_range(self):
        cmpt = 0
        i = 0
        val = 0
        result = {}
        range = param.RANGE_COLLISIONS_GRAPH
        while i < len(self.border_collisions):
            j = 0
            while i < len(self.border_collisions) and j < range:
                val += self.border_collisions[i]
                j += 1
                i += 1
            val /= j
            result[int(i/range)-1] = val
        return result

    border_collision_range = property(_get_border_collision_range)
