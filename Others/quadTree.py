

class QuadTree:

    def __init__(self, dim, depth):
        self.location = 0
        self.nodes = []

        for i in range(dim):
            if depth != 0:
                self.nodes.append(QuadTree(dim, depth-1))

    def add(self, other):
        return self.nodes.append(other)

    def remove(self, other):
        self.nodes.remove(other)

    def __iter__(self):
        return self

    def __next__(self):
        if self.location == len(self.nodes):
            self.location = 0
            raise StopIteration
        value = self.nodes[self.location]
        self.location += 1
        return value
