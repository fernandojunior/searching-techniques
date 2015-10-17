'''
Nearest Neighbour Algorithm
Adapted from Vicente J. Ferrer Dalmau
https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/NearestNeighbour.java
'''
from datetime import datetime
import json


def read_graph(path):
    '''
    Open a json file that contains the edge costs
    '''
    with open(path) as f:
        return json.load(f)


class Graph:
    '''
    Graph with edge costs.
    '''
    def __init__(self, graph):
        self.graph = graph

    def cost(self, from_node, to_node):
        return self.graph[from_node][to_node]

    def vertex(self, position):
        return self.vertices()[position]

    def vertices(self):
        return list(self.graph.keys())


class NearestNeighbour:

    def __init__(self, sourceCity, distances):
        '''
        Creates a new instance of NearestNeighbour
        '''
        self.sourceCity = sourceCity
        self.distances = distances
        self.followedRoute = []
        self.nodes = 0
        self.routeCost = 0

    def execute(self):
        '''
        Executes the algorithm
        '''

        self.followedRoute.append(self.sourceCity)
        self.nodes += 1

        startTime = datetime.now()
        self.search(self.sourceCity)
        endTime = datetime.now()

        print('DEPTH FIRST SEARCH\n\n')
        print(
            "\nBetter solution:",
            self.followedRoute,
            "// Cost:", self.routeCost, "\n")
        print("Visited Nodes:", self.nodes, "\n")
        print("Elapsed Time:", str(endTime - startTime), "ms\n")

    def search(self, from_node):
        '''
        @from: node where we start the search.
        '''

        currentTown = from_node

        while self.nodes != len(self.distances.vertices()):
            # choose the closest town
            lowestDistance = float('Inf')
            chosen = None
            for nextTown in self.distances.vertices():
                if nextTown not in self.followedRoute:
                    tempDistance = self.distances.cost(currentTown, nextTown)
                    if tempDistance < lowestDistance:
                        lowestDistance = tempDistance
                        chosen = nextTown

            self.routeCost += lowestDistance
            self.followedRoute.append(chosen)
            currentTown = chosen
            self.nodes += 1

        # add the last town
        self.routeCost += self.distances.cost(currentTown, self.sourceCity)
        self.followedRoute.append(self.sourceCity)
        self.nodes += 1

graph = read_graph('data/brazil58.json')
graph = Graph(graph)
solution = NearestNeighbour('0', graph)
solution.execute()
