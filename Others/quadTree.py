

class QuadTree:

    def __init__(self, dim, depth):

        self.nodes = []

        for i in range(dim):
            if depth != 0:
                self.nodes.append(QuadTree(dim, depth-1))

    def add(self, other):
        return self.nodes.append(other)

    def remove(self, other):
        self.nodes.remove(other)
