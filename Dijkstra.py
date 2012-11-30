class Graph(object):
    """
    A simple undirected, weighted graph
    """
    def __init__(self):
        #initialize the nodes, edges and distances of the graph
        self.nodes = set()
        self.edges = {}
        self.distances = {}
    
    def add_node(self, value):
        self.nodes.add(value)
    
    def add_edge(self, from_node, to_node, distance):
        #add the edge both between from/to and to/from
        self._add_edge(from_node, to_node, distance)
        self._add_edge(to_node, from_node, distance)

    def _add_edge(self, from_node, to_node, distance):
        
        self.edges.setdefault(from_node, [])
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial_node):
    visited = {initial_node: 0}
    path = {}
    
    nodes = set(graph.nodes)
    count = {}
    for node in nodes:
        count[node] = 1
    
    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        cur_wt = visited[min_node]
        
        print min_node
        print cur_wt
        for edge in graph.edges[min_node]:
            if (cur_wt == 0):
                wt = cur_wt + graph.distances[(min_node, edge)]
            else:
                print count[min_node], graph.distances[(min_node, edge)]
                wt = float(cur_wt*count[min_node] + graph.distances[(min_node, edge)])/(count[min_node] + 1)
            if (edge not in visited or wt < visited[edge]) and path.get(min_node, -1) != edge:
                if edge in visited and wt < visited[edge]:
                    count[edge] = count[edge] + 1
                print 'changing to new weight for', edge, wt
                visited[edge] = wt
                path[edge] = min_node
                
                
            else:
                print 'not changing to new weight for', edge, wt
                
        print '---------------'
    
    return visited, path

def shortest_path(graph, initial_node, goal_node):
    distances, paths = dijkstra(graph, initial_node)
    print distances
    print paths
    route = [goal_node]

    while goal_node != initial_node:
        route.append(paths[goal_node])
        goal_node = paths[goal_node]

    route.reverse()
    return route


if __name__ == '__main__':
    g = Graph()
    g.nodes = set(range(1, 7))
    g.add_edge(1, 2, 7)
    g.add_edge(1, 3, 9)
    g.add_edge(1, 6, 14)
    g.add_edge(2, 3, 10)
    g.add_edge(2, 4, 15)
    g.add_edge(3, 4, 11)
    g.add_edge(3, 6, 2)
    g.add_edge(4, 5, 6)
    g.add_edge(5, 6, 9)
    shortest_path(g, 1, 5)
    assert shortest_path(g, 1, 5) == [1, 3, 6, 5]
    assert shortest_path(g, 5, 1) == [5, 6, 3, 1]
    assert shortest_path(g, 2, 5) == [2, 3, 6, 5]
    assert shortest_path(g, 1, 4) == [1, 3, 4] 