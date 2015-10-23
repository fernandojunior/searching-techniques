'''
Nearest Neighbour Algorithm to find shortest path.

@author Fernando Felix do Nascimento Junior

@links
    https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/NearestNeighbour.java
'''
from datetime import datetime
from graph import Graph


class NearestNeighbour:

    def __init__(self, start, graph):
        '''
        Solution of shortest path problem using nearest neighbour algorithm
        '''
        self.start = start
        self.graph = graph
        self.followedRoute = []
        self.routeCost = 0

    def nearest_neighbour(self, origin, neighbours):
        '''
        Returns the nearest neighbour of a vertice origin
        '''
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
        missing = list(self.graph.vertices())  # towns to be visited
        currentTown = self.start
        self.followedRoute.append(currentTown)
        missing.remove(currentTown)

        while len(missing) > 0:
            closest = self.nearest_neighbour(currentTown, missing)
            self.followedRoute.append(closest)
            self.routeCost += self.graph.cost(currentTown, closest)
            currentTown = closest
            missing.remove(currentTown)  # remove visited town

        # add the last one
        self.followedRoute.append(self.start)
        self.routeCost += self.graph.cost(currentTown, self.start)


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = Graph('data/test.json')
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

test()
