import io
import copy
import json


def convert(data):
    """Convert a data to a graph structure"""
    if isinstance(data, (dict)):
        return copy.deepcopy(data)
    elif isinstance(data, str):  # it's a json file path
        with open(data) as f:
            return convert(f)
    elif isinstance(data, io.TextIOBase):  # it's a json file
        return json.load(data)
    else:
        raise TypeError('Unsupported data type.')


class Graph:
    """
    Read-only graph of costs.
    """

    def __init__(self, data):
        """
        :data: Data to initialize the graph. The data must be a dict of dicts.
        """
        self.__graph = convert(data)

    def cost(self, a, b):
        return self.graph[a][b]

    def edges(self, vertex):
        return self.graph[vertex]

    def neighbors(self, vertex):
        return self.edges(vertex).keys()

    def path_cost(self, path):
        cost = 0
        for i in range(len(path) - 1):
            cost += self.cost(path[i], path[i + 1])
        return cost

    def size(self):
        return len(self.graph.keys())

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())

    @property
    def graph(self):
        return self.__graph
