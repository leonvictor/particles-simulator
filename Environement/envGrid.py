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

    def add(self, envObj):
        grid_pos = envObj.position//self.side
        grid_pos = EnvGrid.totuple(grid_pos)

        envObj.gridPos = grid_pos
        envObj.envGrid = self

        if grid_pos in self.grid.keys():
            self.grid[grid_pos].append(envObj)
        else:
            self.grid[grid_pos] = [envObj]

    def remove(self, envObj):
        self.grid[envObj.gridPos].remove(envObj)
        if len(self.grid[envObj.gridPos]) == 0 :
            del self.grid[envObj.gridPos]

        envObj.envGrid = None

    def moved(self, envObj):
        grid_pos = envObj.position // self.side
        grid_pos = EnvGrid.totuple(grid_pos)

        if grid_pos != envObj.gridPos:
            self.remove(envObj)
            self.add(envObj)

    def getBounds(self):

        boundsMin = list(list(self.grid.keys())[0])
        boundsMax = list(boundsMin)
        boundsAgentMin = list(self.grid[list(self.grid.keys())[0]][0].position)
        boundsAgentMax = list(boundsAgentMin)

        for pos in self.grid.keys():
            for i in range(len(pos)):
                if boundsMax[i] <= pos[i]:
                    boundsMax[i] = pos[i]
                    for agent in self.grid[pos]:
                        if agent.position[i] > boundsAgentMax[i]:
                            boundsAgentMax[i] = agent.position[i]
                if boundsMin[i] >= pos[i]:
                    boundsMin[i] = pos[i]
                    for agent in self.grid[pos]:
                        if agent.position[i] < boundsAgentMin[i]:
                            boundsAgentMin[i] = agent.position[i]

        print((boundsAgentMin, boundsAgentMax))
        return boundsAgentMin, boundsAgentMax

    @staticmethod
    def totuple(a):
        try:
            return tuple(EnvGrid.totuple(i) for i in a)
        except TypeError:
            return a

    def getListFromRank(self, gridPos, rank):
        list = self.buildList(gridPos, rank, len(gridPos),0)
        tupleList = EnvGrid.totuple(list)
        result = []
        for i in tupleList:
            if i in self.grid.keys():
                result.extend(self.grid[i])
        return result

    def buildList(self, gridPos, rank, leng, i):
        if(i == leng):
            return gridPos

        listBase = []

        for cmpt in range(0, i):
                listBase.append(gridPos[cmpt])

        listOfLists = []

        for j in range(int(gridPos[i]-rank), int(gridPos[i]+rank+1)):
            listBaseCopy = list(listBase)
            listBaseCopy.append(j)
            m = leng - (len(listBaseCopy))
            for k in range(0, m):
                listBaseCopy.append(0)
            listOfLists.append(listBaseCopy)

        if (i + 1 == leng):
            return listOfLists

        result = []

        for el in listOfLists:
            result.extend(self.buildList(el, rank, leng, i+1))

        return result



    def save(self, name):

        fieldnames = ['case, nb_agents']

        data = []

        for a in self.grid.items():
            b = [a[0], len(a[1])]
            data.append(b)

        os.makedirs(self.path, exist_ok=True)

        cmpt = 0
        while Path(EnvGrid.path + name + str(cmpt) + EnvGrid.extension).is_file():
            cmpt += 1

        EnvGrid.WriteListToCSV(self.path + name + str(cmpt) + self.extension, fieldnames, data)

    def load(name):
        datalist = EnvGrid.ReadCSVasList( EnvGrid.path + name)

        result = {}

        for item in datalist:
            if len(item) != 2:
                continue

            result[make_tuple(item[0])] = item[1]

        return result


    def WriteListToCSV(csv_file, csv_columns, data_list):

        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)

    def ReadCSVasList(csv_file):
        with open(csv_file) as csvfile:
            reader = csv.reader(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            datalist = list(reader)
            return datalist
        return None