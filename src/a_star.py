'''
Vicente J. Ferrer Dalmau

Implementation of the A* (A Star) algorithm.

http://www.redblobgames.com/pathfinding/a-star/implementation.html
https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/AStar.java
http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
https://en.wikipedia.org/wiki/A%2a_search_algorithm
http://www.bogotobogo.com/python/python_PriorityQueue_heapq_Data_Structure.php
'''
from datetime import datetime
from queue import PriorityQueue


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


class Town:

    def __init__(self, number, g, h, level, parent=None):
        '''
        Creates a new instance of Town
        '''
        self.number = number
        self.g = g
        self.h = h
        self.level = level
        self.f = self.g + self.h
        self.parent = parent

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f


class AStar:

    # Estimation of the cost between two cities, it can overestimate the real
    # value (h' > h), so the algorithm it's not optimum.
    HEURISTICCONSTANT = 15

    def __init__(self, sourceCity, graph):
        '''
        Creates a new instance of AStar
        '''
        self.distances = graph
        self.sourceCity = sourceCity
        self.opened = PriorityQueue()
        self.optimumRoute = []
        self.optimumCost = float('Inf')
        self.cities_size = len(self.distances.vertices())

    def getHeuristicValue(self, level):
        '''
        Gets the heuristic value for a given depth
        The level 0 has the maximum value.
        '''
        return self.HEURISTICCONSTANT * (self.cities_size - level)

    def execute(self):
        '''
        executes the algorithm
        '''

        cities_size = self.cities_size

        # have we found the solution?
        solution = False

        # start the timer
        startTime = datetime.now()

        # initial town
        self.opened.put(Town(self.sourceCity, 0, self.getHeuristicValue(0), 0))

        while (not self.opened.empty()) and (not solution):
            # gets the city with lower g value
            currentTown = self.opened.get()

            # rebuild the followed route for the selected town
            aux = currentTown
            followedRoute = [aux.number]
            while aux.level is not 0:
                aux = aux.parent
                followedRoute.insert(0, aux.number)

            if currentTown.level == cities_size:
                solution = True
                optimumRoute = followedRoute
                optimumCost = currentTown.g

            else:
                for i in self.distances.vertices():
                    # have we visited this city in the current followed route?
                    visited = i in followedRoute
                    isSourceCity = i == self.sourceCity
                    isSolution = len(followedRoute) == cities_size and isSourceCity

                    if not visited or isSolution:
                        cost = self.distances.cost(currentTown.number, i)
                        print(cost)
                        g = currentTown.g + cost
                        h = self.getHeuristicValue(currentTown.level + 1)
                        level = currentTown.level + 1
                        childTown = Town(i, g, h, level)
                        childTown.parent = currentTown
                        self.opened.put(childTown)

        endTime = datetime.now()

        elapsed_time = endTime - startTime

        print("Elapsed Time:", str(elapsed_time), "ms")
        print("Cost:", optimumCost)
        print("Path:", optimumRoute)

graph = {
    "0": {
        "0": 0,
        "1": 2635.0,
        "2": 2713.0,
        "3": 2437.0
    },
    "1": {
        "0": 2635.0,
        "1": 0,
        "2": 314.0,
        "3": 2636.0
    },
    "2": {
        "0": 2713.0,
        "1": 314.0,
        "2": 0,
        "3": 2730.0,
    },
    "3": {
        "0": 2437.0,
        "1": 2636.0,
        "2": 2730.0,
        "3": 0
    }}

graph = Graph(graph)

AStar('0', graph).execute()
