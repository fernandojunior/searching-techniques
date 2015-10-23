'''
Nearest Neighbour Algorithm to find shortest path.

@author Fernando Felix do Nascimento Junior

@links
    https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/NearestNeighbour.java
'''
from datetime import datetime
from graph import Graph


class NearestNeighbour:

    def __init__(self, start, stop, graph):
        '''
        Creates a new instance of NearestNeighbour
        '''
        self.start = start
        self.stop = stop
        self.graph = graph
        self.followedRoute = []
        self.routeCost = 0

    def nearest_neighbour(self, origin, neighbours):
        lowest_cost = float('Inf')
        nearest = None

        for neighbour in neighbours:
            cost = self.graph.cost(origin, neighbour)
            if cost < lowest_cost:
                lowest_cost = cost
                nearest = neighbour

        return nearest

    def solve(self):
        '''
        Executes the algorithm
        '''
        missing_towns = list(self.graph.vertices())  # towns to be visited
        missing_towns.remove(self.start)
        # missing_towns.remove(self.stop)

        currentTown = self.start
        self.followedRoute.append(currentTown)

        while len(missing_towns) > 0:
            closest = self.nearest_neighbour(currentTown, missing_towns)
            self.followedRoute.append(closest)
            self.routeCost += self.graph.cost(currentTown, closest)
            missing_towns.remove(closest)  # remove visited town
            currentTown = closest

        # add the last town
        self.followedRoute.append(self.start)
        self.routeCost += self.graph.cost(currentTown, self.start)


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = Graph('data/test.json')
        solution = NearestNeighbour('0', '0', graph)
        start_time = datetime.now()
        solution.solve()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Elapsed Time:", str(elapsed_time), "ms")
        print("Cost:", solution.routeCost)
        print("Path:", solution.followedRoute)
        results.append([elapsed_time, solution])

    return results

test()
