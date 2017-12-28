import csv
import os
from pathlib import Path
from ast import literal_eval as make_tuple


class EnvGrid:

    path = os.getcwd() + "\\csv\\stat_data\\"
    extension = ".csv"

    def __init__(self, side):
        self.side = side
        self.grid = {}

    def add(self, env_obj):
        grid_pos = env_obj.position // self.side
        grid_pos = EnvGrid.to_tuple(grid_pos)
        env_obj.gridPos = grid_pos
        env_obj.envGrid = self

        if grid_pos in self.grid.keys():
            self.grid[grid_pos].append(env_obj)
        else:
            self.grid[grid_pos] = [env_obj]

    def remove(self, env_obj):
        self.grid[env_obj.gridPos].remove(env_obj)
        if len(self.grid[env_obj.gridPos]) == 0:
            del self.grid[env_obj.gridPos]

        env_obj.envGrid = None

    def moved(self, env_obj):
        grid_pos = env_obj.position // self.side
        grid_pos = EnvGrid.to_tuple(grid_pos)

        if grid_pos != env_obj.gridPos:
            self.remove(env_obj)
            self.add(env_obj)

    def get_bounds(self):

        bounds_min = list(list(self.grid.keys())[0])
        bounds_max = list(bounds_min)
        bounds_agent_min = list(self.grid[list(self.grid.keys())[0]][0].position)
        bounds_agent_max = list(bounds_agent_min)

        for pos in self.grid.keys():
            for i in range(len(pos)):
                if bounds_max[i] <= pos[i]:
                    bounds_max[i] = pos[i]
                    for agent in self.grid[pos]:
                        if agent.position[i] > bounds_agent_max[i]:
                            bounds_agent_max[i] = agent.position[i]
                if bounds_min[i] >= pos[i]:
                    bounds_min[i] = pos[i]
                    for agent in self.grid[pos]:
                        if agent.position[i] < bounds_agent_min[i]:
                            bounds_agent_min[i] = agent.position[i]

        return bounds_agent_min, bounds_agent_max

    @staticmethod
    def to_tuple(a):
        try:
            return tuple(EnvGrid.to_tuple(i) for i in a)
        except TypeError:
            return a

    def get_list_from_rank(self, grid_pos, rank):
        l = self.build_list(grid_pos, rank, len(grid_pos), 0)
        tuple_list = EnvGrid.to_tuple(l)
        result = []
        for i in tuple_list:
            if i in self.grid.keys():
                result.extend(self.grid[i])
        return result

    def build_list(self, grid_pos, rank, lenght, i):
        if i == lenght:
            return grid_pos
        list_base = []
        for cmpt in range(0, i):
                list_base.append(grid_pos[cmpt])
        list_of_lists = []
        for j in range(int(grid_pos[i] - rank), int(grid_pos[i] + rank + 1)):
            list_base_copy = list(list_base)
            list_base_copy.append(j)
            m = lenght - (len(list_base_copy))
            for k in range(0, m):
                list_base_copy.append(0)
            list_of_lists.append(list_base_copy)
        if i + 1 == lenght:
            return list_of_lists
        result = []
        for el in list_of_lists:
            result.extend(self.build_list(el, rank, lenght, i + 1))
        return result

    def save(self, name):

        field_names = ['case, nb_agents']

        data = []

        for a in self.grid.items():
            b = [a[0], len(a[1])]
            data.append(b)

        os.makedirs(self.path, exist_ok=True)

        cmpt = 0
        while Path(EnvGrid.path + name + str(cmpt) + EnvGrid.extension).is_file():
            cmpt += 1

        EnvGrid.write_list_to_csv(self.path + name + str(cmpt) + self.extension, field_names, data)

    @staticmethod
    def load(name):
        data_list = EnvGrid.read_csv_as_list(EnvGrid.path + name)

        result = {}

        for item in data_list:
            if len(item) != 2:
                continue

            result[make_tuple(item[0])] = item[1]

        return result

    @staticmethod
    def write_list_to_csv(csv_file, csv_columns, data_list):

        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)

    @staticmethod
    def read_csv_as_list(csv_file):
        with open(csv_file) as csvfile:
            reader = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            datalist = list(reader)
            return datalist
        return None

