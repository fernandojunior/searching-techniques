import json


class Graph:
    '''
    Graph of costs.
    '''
    def __init__(self, graph):
        if isinstance(graph, dict):
            self.graph = graph
        elif isinstance(graph, str):  # it's a json file path
            with open(graph) as f:
                self.graph = json.load(f)
        elif isinstance(graph, file):  # it's a json file
            self.graph = json.load(graph)
        else:
            raise TypeError('Unsupported argument type.')

    def cost(self, a, b):
        return self.graph[a][b]

    def edges(self, vertex):
        return self.graph[vertex]

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
