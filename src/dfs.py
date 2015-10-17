'''
Depth First Search Algorithm to find shortest path.
Adapted from Vicente J. Ferrer Dalmau.

@author Fernando Felix do Nascimento Junior

@links
    https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/DepthFirstSearch.java?r=13
'''
from datetime import datetime


class DepthFirstSearch:

    # Creates a new instance of DepthFirstSearch
    def __init__(self, distances, sourceCity):
        self.distances = distances
        self.sourceCity = sourceCity
        self.optimumRoute = []
        self.nodes = 0
        self.routeCost = 0
        self.optimumCost = float('Inf')

    def execute(self):
        '''
        executes the algorithm
        '''
        initialRoute = [self.sourceCity]
        self.nodes = self.nodes + 1

        startTime = datetime.now()
        self.search(self.sourceCity, initialRoute)
        endTime = datetime.now()

        print('DEPTH FIRST SEARCH\n\n')
        print(
            "\nBetter solution:",
            self.optimumRoute,
            "// Cost:", self.optimumCost, "\n")
        print("Visited Nodes:", self.nodes, "\n")
        print("Elapsed Time:", str(endTime - startTime), "ms\n")

    def cost(self, from_node, to_node):
        '''
        edge cost (between two nodes)
        '''
        return self.distances[from_node][to_node]

    def search(self, from_node, followedRoute):
        '''
         @param from node where we start the search.
         @param route followed route for arriving to node "from".
        '''

        # we've found a new solution
        if (len(followedRoute) == len(self.distances)):

            followedRoute.append(self.sourceCity)
            self.nodes = self.nodes + 1

            # update the route's cost
            self.routeCost = self.routeCost + self.cost(from_node, self.sourceCity)

            if (self.routeCost < self.optimumCost):
                self.optimumCost = self.routeCost
                self.optimumRoute = list(followedRoute)  # copy

            print(followedRoute, "// Cost:", self.routeCost, "\n")

            # update the route's cost (back to the previous value)
            self.routeCost = self.routeCost - self.cost(from_node, self.sourceCity)
        else:
            for to_node in range(len(self.distances)):
                if to_node not in followedRoute:
                    increasedRoute = list(followedRoute)  # copy
                    increasedRoute.append(to_node)
                    self.nodes = self.nodes + 1

                    # update the route's cost
                    self.routeCost = self.routeCost + self.cost(from_node, to_node)

                    self.search(to_node, increasedRoute)

                    # update the route's cost (back to the previous value)
                    self.routeCost = self.routeCost - self.cost(from_node, to_node)

'''
sourceCity = 0
distances = {
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
DepthFirstSearch(distances, sourceCity).execute()
'''
