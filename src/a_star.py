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
    """Contains all the important information (cost) about a Town."""

    def __init__(self, name, g=None, h=None, parent=None):
        #: The name of the town.
        self.name = name

        #: The cost of getting from the start town to this.
        self.g = g

        #: The heuristic estimate of the cost to get from this town to goal.
        self.h = h

        #: Previous town.
        self.parent = parent

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    @property
    def f(self):
        """Cost function f"""
        return self.g + self.h

    @property
    def level(self):
        """Towns travelled to reach this one"""
        return 0 if not self.parent else self.parent.level + 1


class AStar:
    """Implementation of the A* (A Star) algorithm."""

    #: Estimation of the cost between two cities, it can overestimate the real
    #: value (h' > h), so the algorithm it's not optimum.
    HEURISTICCONSTANT = 15

    def __init__(self, start, graph):
        #: The start city of route.
        self.start = start

        #: A graph with vertices and edge costs.
        self.distances = graph

        #: Stores the optimum route
        self.optimum_route = []

        #: Stores optimum cost
        self.optimum_cost = float('Inf')

        #: Total cities to visit
        self.cities_size = self.distances.size()

    def heuristic_cost(self, level):
        """Returns the heuristic cost estimate for a given city level."""
        return self.HEURISTICCONSTANT * (self.cities_size - level)

    def were_all_cities_visited(self, route):
        """Verifies if all cities were visited."""
        return len(route) == self.cities_size

    def is_end_city(self, city_name, route):
        """Verifies if a city is the end of the route."""
        return self.were_all_cities_visited(route) and city_name == self.start

    def cost(self, from_, to_):
        """Returns the cost (distance) between two cities"""
        return self.distances.cost(from_, to_)

    def solve(self):
        """Executes the algorithm."""

        # The set of tentative nodes to be evaluated
        opened = PriorityQueue()

        # Initially containing the start city.
        opened.put(Town(self.start, 0, self.heuristic_cost(0)))

        while True:
            # Get the city with lower f cost (highest priority)
            current = opened.get()

            # rebuild the followed route for the current town
            aux = current
            followed_route = [aux.name]
            while aux.level is not 0:
                aux = aux.parent
                followed_route.insert(0, aux.name)

            # Was the route completed? start == end?
            if current.level == self.cities_size:
                self.optimum_route = followed_route
                self.optimum_cost = current.g
                break

            for name in self.distances.vertices():
                if (name not in followed_route or
                        self.is_end_city(name, followed_route)):
                    neighbor = Town(name, parent=current)
                    neighbor.g = current.g + self.cost(current.name, name)
                    neighbor.h = self.heuristic_cost(neighbor.level)
                    opened.put(neighbor)


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
        print("Cost:", solution.optimum_cost)
        print("Path:", solution.optimum_route)
        results.append([elapsed_time, solution])

    return results

test()
