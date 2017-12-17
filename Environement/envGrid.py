import csv
import os
from pathlib import Path

class EnvGrid:

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

        path = os.getcwd() + "\\csv"

        os.makedirs(path, exist_ok=True)

        path += "\\" + name
        extension = ".csv"
        cmpt = 0
        while Path(path + str(cmpt) + extension).is_file():
            cmpt += 1

        self.WriteListToCSV(path + str(cmpt) + extension, fieldnames, data)


    def WriteListToCSV(self, csv_file, csv_columns, data_list):

        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)