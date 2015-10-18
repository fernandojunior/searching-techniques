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

    def search(self, current, followedRoute=[]):
        '''
         @param current current vertex where we start the search.
         @param followedRoute for arriving to current vertex.
        '''
        if current not in followedRoute:
            followedRoute.append(current)

        # we've found a complete route
        if (len(followedRoute) == len(self.vertices)):
            followedRoute.append(self.start)  # end city
            routeCost = self.graph.path_cost(followedRoute)

            if (routeCost < self.optimumCost):
                self.optimumCost = routeCost
                self.optimumRoute = followedRoute
        else:
            for target in self.vertices:
                if target not in followedRoute:
                    self.search(target, list(followedRoute))


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
