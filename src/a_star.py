"""
This module implements the A* (A Star) algorithm.
It is based on Vicente J. Ferrer Dalmau code [#]_.

..[#] https://code.google.com/p/tspuib/

:author: Fernando Felix do Nascimento Junior
"""
from datetime import datetime
from queue import PriorityQueue
from graph import Graph


class CityCost:
    """Contains all the important information (cost) about a city."""

    def __init__(self, city, g=None, h=None, parent=None):
        #: The city
        self.city = city

        #: The cost of getting from the start city to this.
        self.g = g

        #: The heuristic estimate of the cost to get from this city to goal.
        self.h = h

        #: Previous city.
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
        """Cities travelled to reach this one"""
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

    def cost(self, from_, to_):
        """Returns the cost (distance) between two cities"""
        return self.distances.cost(from_, to_)

    def heuristic_cost(self, level):
        """Returns the heuristic cost estimate for a given city level."""
        return self.HEURISTICCONSTANT * (self.cities_size - level)

    def were_all_cities_visited(self, route):
        """Verifies if all cities were visited."""
        return len(route) == self.cities_size

    def is_end_city(self, city, route):
        """Verifies if a city is the end of the route."""
        return self.were_all_cities_visited(route) and city == self.start

    def city_cost(self, city, parent=None):
        """Estimates city cost using information of previous city."""
        cost = CityCost(city, parent=parent)
        cost.g = parent.g + self.cost(parent.city, city) if parent else 0
        cost.h = self.heuristic_cost(cost.level)
        return cost

    def solve(self):
        """Executes the algorithm."""

        # The set of tentative cities cost to be evaluated
        opened = PriorityQueue()

        # Initially containing the start city cost.
        opened.put(self.city_cost(self.start))

        while True:
            # Get the city with lower f cost (highest priority)
            current = opened.get()

            # rebuild the followed route for the current city
            aux = current
            followed_route = [aux.city]
            while aux.level is not 0:
                aux = aux.parent
                followed_route.insert(0, aux.city)

            # Was the route completed? start == end?
            if current.level == self.cities_size:
                self.optimum_route = followed_route
                self.optimum_cost = current.g
                break

            for neighbor in self.distances.edges(current.city):
                if (neighbor not in followed_route or
                        self.is_end_city(neighbor, followed_route)):
                    opened.put(self.city_cost(neighbor, current))


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
