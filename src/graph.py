import json


def read_graph(path):
    '''
    Open a json file that contains the edge costs
    '''
    with open(path) as f:
        return json.load(f)


class Graph:
    '''
    Graph of costs.
    '''
    def __init__(self, graph):
        self.graph = graph

    def cost(self, a, b):
        return self.graph[a][b]

    def edges(self, vertex):
        return self.graph[vertex]

    def path_cost(self, path):
        cost = 0
        for i in range(len(path) - 1):
            cost += self.cost(path[i], path[i + 1])
        return cost

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())
