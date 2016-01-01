"""
This module implements the A* (A Star) algorithm.
It is based on Vicente J. Ferrer Dalmau code [#]_. It's not optimum.

..[#] https://code.google.com/p/tspuib/

:author: Fernando Felix do Nascimento Junior
"""
from datetime import datetime
# from queue import PriorityQueue
from graph import Graph

import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def put(self, item, priority):
        heapq.heappush(self.queue, (priority, item))

    def get(self):
        return heapq.heappop(self.queue)[1]


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(int(a) - int(b)) + abs(int(a) - int(b))


class Node:
    def __init__(self, node, h=None, g=None, f=None):
        self.node = node
        self.h = h
        self.g = g
        self.f = f

    def __repr__(self):
        return self.node


class AStar:

    def __init__(self, start, graph):
        self.start = start
        self.graph = graph

    def lowest_cost(self, origin, neighbors):
        h = float('Inf')
        g = 0
        f = h + g
        nearest = None

        for neighbour in neighbors:
            if neighbour == origin.node:
                continue
            nh = heuristic(origin.node, neighbour)
            ng = (origin.g or 0) + self.graph.cost(origin.node, neighbour)
            nf = nh + ng
            if nf < f:
                h = nh
                g = ng
                f = nf
                nearest = neighbour

        return Node(nearest, h, g, f)

    def run(self):
        missing = list(self.graph.vertices())  # towns to be visited
        route = []

        current = Node(self.start)
        route.append(current.node)
        missing.remove(current.node)

        while len(missing) > 0:
            current = self.lowest_cost(current, missing)
            route.append(current.node)
            missing.remove(current.node)  # remove visited town

            # going back to start city
            if current.node is not self.start and len(missing) == 0:
                missing.append(self.start)

        return route, current.g


def test(max_runs=1):

    for run in range(max_runs):
        print('Run:', run)
        graph = Graph('data/test.json')
        start_time = datetime.now()
        came_from, cost_so_far = AStar('0', graph).run()
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Elapsed Time:", str(elapsed_time), "ms")
        print("Cost:", cost_so_far)
        print("Path:", came_from)

test()
