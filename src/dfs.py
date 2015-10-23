'''
Depth First Search Algorithm to find shortest path.

@author Fernando Felix do Nascimento Junior

@links
    https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/DepthFirstSearch.java?r=13
'''
from datetime import datetime
from graph import Graph


class DepthFirstSearch:

    def __init__(self, start, graph):
        self.graph = graph  # graph with vertices and edge costs
        self.start = start  # start city
        self.vertices = self.graph.vertices()  # cities to visit
        self.optimum_route = []
        self.optimum_cost = float('Inf')

    def solve(self):
        '''
        executes the algorithm
        '''
        self.search(self.start)

    def search(self, current, followed=[], missing=None):
        '''
        Searches for possible solutions
        @param current Current vertex where we start the search.
        @param followed Followed route for arriving to current vertex.
        @param missing List of neighbors of current vertex to be visited
        '''
        missing = missing or list(self.vertices)

        if current not in followed:
            followed.append(current)

        missing.remove(current)  # current already visited

        for neighbor in missing:  # neighbors to visit
            self.search(neighbor, list(followed), list(missing))

        # we've found a complete route (possible solution)
        if not missing:  # list is empty
            followed.append(self.start)  # end city
            routeCost = self.graph.path_cost(followed)

            if (routeCost < self.optimum_cost):
                self.optimum_cost = routeCost
                self.optimum_route = followed


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = Graph('data/test.json')
        solution = DepthFirstSearch('0', graph)
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
