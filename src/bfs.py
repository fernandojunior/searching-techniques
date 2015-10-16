# graph is in adjacent list representation
graph = {
    '1': ['2', '3', '4'],
    '2': ['5', '6'],
    '5': ['9', '10'],
    '4': ['7', '8'],
    '7': ['11', '12']}

graph2 = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']}


def bfs(graph, start, end):
    '''
    http://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
    '''
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        print('queue %s' % queue)
        # get the first path from the queue
        path = queue.pop(0)
        print('path %s' % path)
        # get the last node from the path
        node = path[-1]
        print('node %s' % node)
        # path found
        if node == end:
            # enumerate all adjacent nodes,
            # construct a new path and push it into the queue
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)
        print()

# print(bfs(graph, '1', '11'))
# bfs(graph2, 'A', 'F')
bfs(graph, '1', '11')
