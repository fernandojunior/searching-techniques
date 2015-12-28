"""
This module implements the A* (A Star) algorithm.
It is based on Vicente J. Ferrer Dalmau code [#]_.

..[#] https://code.google.com/p/tspuib/

:author: Fernando Felix do Nascimento Junior
"""
from datetime import datetime
from queue import PriorityQueue
from graph import Graph


class Town:
    """
    Contains all the important information about a Town.
    """

    def __init__(self, id, g=None, h=None, parent=None):
        #: The identification of the town.
        self.id = id

        #: The cost of getting from the start town to this.
        self.g = g

        #: The heuristic estimate of the cost to get from this to goal town.
        self.h = h

        #: Previous town.
        self.parent = parent

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    @property
    def f(self):
        """
        Cost function f
        """
        return self.g + self.h

    @property
    def level(self):
        """
        Towns travelled to reach this town
        """
        return 0 if not self.parent else self.parent.level + 1


class AStar:
    """
    Implementation of the A* (A Star) algorithm.
    """

    #: Estimation of the cost between two cities, it can overestimate the real
    #: value (h' > h), so the algorithm it's not optimum.
    HEURISTICCONSTANT = 15

    def __init__(self, start, graph):
        #: The start city of route.
        self.start = start

        #: A graph with vertices and edge costs.
        self.graph = graph

        #: The set of tentative nodes to be evaluated, initially containing the
        #: start node.
        self.opened = PriorityQueue()

        #: Stores the optimum route
        self.optimumRoute = []

        #: Stores optimum cost
        self.optimumCost = float('Inf')

        #: Total cities to visit
        self.cities_size = len(self.graph.vertices())

    def get_heuristic_value(self, level):
        """
        Gets the heuristic value for a given town level.
        The level 0 has the maximum value.
        """
        return self.HEURISTICCONSTANT * (self.cities_size - level)

    def is_route_complete(self, followedRoute):
        """
        Verify if the route is complete.
        """
        return len(followedRoute) == self.cities_size

    def solve(self):
        """
        Executes the algorithm
        """
        # initial town
        self.opened.put(Town(self.start, 0, self.get_heuristic_value(0)))

        while True:
            # get the city with lower f value (highest priority)
            currentTown = self.opened.get()

            # rebuild the followed route for the selected town
            aux = currentTown
            followedRoute = [aux.id]
            while aux.level is not 0:
                aux = aux.parent
                followedRoute.insert(0, aux.id)

            # Was the route completed? start == end?
            if currentTown.level == self.cities_size:
                self.optimumRoute = followedRoute
                self.optimumCost = currentTown.g
                break  # we found the solution

            for i in self.graph.vertices():
                if (i not in followedRoute or
                        self.is_route_complete(followedRoute) and
                        i == self.start):
                    cost = self.graph.cost(currentTown.id, i)
                    childTown = Town(i, parent=currentTown)
                    childTown.g = childTown.parent.g + cost
                    childTown.h = self.get_heuristic_value(childTown.level)
                    self.opened.put(childTown)


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = Graph('data/test.json')
        solution = AStar('0', graph)
        start_time = datetime.now()
        solution.solve()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Elapsed Time:", str(elapsed_time), "ms")
        print("Cost:", solution.optimumCost)
        print("Path:", solution.optimumRoute)
        results.append([elapsed_time, solution])

    return results

test()
