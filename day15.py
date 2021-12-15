from utils import parse_data
from collections import defaultdict
from queue import PriorityQueue


def make_map(data):
    return {(row, col): int(data[row][col])
            for row in range(len(data))
            for col in range(len(data[row]))}


def print_map(energy_map):
    loc = list(energy_map.keys())[-1]
    x, y = loc
    for row in range(x + 1):
        for col in range(y + 1):
            print(energy_map[(row, col)], end='')
        print()
    print()


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices*num_of_vertices
        self.edges = defaultdict()
        self.nodes = [(i, j)
                      for i in range(num_of_vertices)
                      for j in range(num_of_vertices)]

    def add_edge(self, u, v, weight):
        if u in self.nodes and v in self.nodes:
            self.edges[(u, v)] = weight

    def add_edge_with_map(self, risk_map):
        for node, risk in risk_map.items():
            for neighbor in self.neighbors(node):
                if neighbor in risk_map:
                    self.edges[(neighbor, node)] = risk

    def neighbors(self, loc):
        x, y = loc
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return [(x + dx, y + dy) for dx, dy in directions]


def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph.nodes}
    prev = {node: None for node in graph.nodes}
    dist[source] = 0
    q = PriorityQueue()
    q.put((0, source))
    while not q.empty():
        u = q.get()[1]
        for v in graph.neighbors(u):
            if ((u, v) in graph.edges and
               dist[v] > dist[u] + graph.edges[(u, v)]):
                dist[v] = dist[u] + graph.edges[(u, v)]
                q.put((dist[v], v))
                prev[v] = u
    return dist, prev


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(
        shortest_path[target_node]))
    print(" -> ".join(str(elem) for elem in reversed(path)))


def solver(risk_map):
    last_element = list(risk_map.keys())[-1]

    graph = Graph(last_element[0] + 1)
    graph.add_edge_with_map(risk_map)

    source = list(risk_map.keys())[0]

    dist, _ = dijkstra(graph, source)
    return dist[last_element]


def day15_1(data):
    risk_map = make_map(data)
    return solver(risk_map)


def below_to_nine(num):
    return num % 9 if num != 9 else 9


def extend_map(risk_map):
    new_risk_map = defaultdict(int)
    dimension = list(risk_map.keys())[-1][0] + 1
    for i in range(5):
        for loc, risk in risk_map.items():
            new_risk_map[(loc[0], loc[1]+i*dimension)] = below_to_nine(risk+i)
    final_map = defaultdict(int)
    for i in range(5):
        for loc, risk in new_risk_map.items():
            final_map[(loc[0] + i*dimension, loc[1])] = below_to_nine(risk+i)
    return final_map


def day15_2(data):
    risk_map = make_map(data)
    risk_map = extend_map(risk_map)
    return solver(risk_map)


if __name__ == '__main__':
    data = parse_data(day=15, parser=str)
    print(day15_1(data))
    print(day15_2(data))
