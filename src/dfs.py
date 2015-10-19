'''
Depth First Search Algorithm to find shortest path.
Adapted from Vicente J. Ferrer Dalmau.

@author Fernando Felix do Nascimento Junior

@links
    https://code.google.com/p/tspuib/source/browse/trunk/TravelingSalesMan/src/travelingsalesman/DepthFirstSearch.java?r=13
'''
from datetime import datetime
from graph import Graph, read_graph


class DepthFirstSearch:

    # Creates a new instance of DepthFirstSearch
    def __init__(self, start, graph):
        self.graph = graph  # graph with vertices and edge costs
        self.start = start  # start city
        self.vertices = self.graph.vertices()  # cities to visit
        self.optimumRoute = []
        self.optimumCost = float('Inf')

    def solve(self):
        '''
        executes the algorithm
        '''
        self.search(self.start)

    def search(self, current, followedRoute=[], missing=None):
        '''
        Searches for possible solutions
        @param current Current vertex where we start the search.
        @param followedRoute Followed route for arriving to current vertex.
        @param missing List of neighbors of current vertex to be visited
        '''
        missing = missing or list(self.vertices)

        if current not in followedRoute:
            followedRoute.append(current)

        missing.remove(current)  # current already visited

        for neighbor in missing:  # neighbors to visit
            self.search(neighbor, list(followedRoute), list(missing))

        # we've found a complete route (possible solution)
        if (len(followedRoute) == len(self.vertices)):
            followedRoute.append(self.start)  # end city
            routeCost = self.graph.path_cost(followedRoute)
            print(followedRoute)

            if (routeCost < self.optimumCost):
                self.optimumCost = routeCost
                self.optimumRoute = followedRoute


def test(max_runs=5):

    results = []

    for run in range(max_runs):
        print('Run:', run)
        graph = read_graph('data/test.json')
        graph = Graph(graph)
        solution = DepthFirstSearch('0', graph)
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
