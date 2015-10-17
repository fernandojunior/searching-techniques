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

    def __init__(self, start, graph):
        '''
        Creates a new instance of NearestNeighbour
        '''
        self.start = start
        self.graph = graph
        self.followedRoute = []
        self.routeCost = 0

    def solve(self):
        '''
        Executes the algorithm
        '''
        self.followedRoute.append(self.start)
        currentTown = self.start

        while len(self.followedRoute) != len(self.graph.vertices()):
            # choose the closest town
            lowestDistance = float('Inf')
            chosen = None
            for nextTown in self.graph.vertices():
                if nextTown not in self.followedRoute:
                    tempDistance = self.graph.cost(currentTown, nextTown)
                    if tempDistance < lowestDistance:
                        lowestDistance = tempDistance
                        chosen = nextTown

            self.routeCost += lowestDistance
            self.followedRoute.append(chosen)
            currentTown = chosen

        # add the last town
        self.routeCost += self.graph.cost(currentTown, self.start)
        self.followedRoute.append(self.start)


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = read_graph('data/brazil58.json')
        graph = Graph(graph)
        solution = NearestNeighbour('0', graph)
        start_time = datetime.now()
        solution.solve()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Elapsed Time:", str(elapsed_time), "ms")
        print("Cost:", solution.routeCost)
        print("Path:", solution.followedRoute)
        results.append([elapsed_time, solution])

    return results
