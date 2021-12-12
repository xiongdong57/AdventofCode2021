from utils import parse_data
from collections import defaultdict


def gen_map(data):
    system = defaultdict(list)
    for start, end in data:
        system[start].append(end)
        system[end].append(start)
    return system


def path_visit(start='start', end='end', system=[], gen_node=None):
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        node = path[-1]
        if node == end:
            yield path
        for next_node in gen_node(node, system, path):
            path2 = path + [next_node]
            frontier.append(path2)


def successors(node, system, path):
    return [node
            for node in system[node]
            if not(node in path and ('a' <= node[0] <= 'z'))]


def successors_v2(node, system, path):
    return [node
            for node in system[node]
            if not(
                (path + [node]).count('start') > 1 or
                (path + [node]).count('end') > 1 or
                (node in path and
                 'a' <= node[0] <= 'z' and
                 is_biger_than_twice(path + [node]))
            )]


def is_biger_than_twice(path):
    smalls = [node
              for node in path
              if 'a' <= node[0] <= 'z']
    return len(smalls) - len(set(smalls)) > 1


def day12_1(data):
    system = gen_map(data)
    paths = list(path_visit(start='start',
                            end='end',
                            system=system,
                            gen_node=successors))
    return len(paths)


def day12_2(data):
    system = gen_map(data)
    paths = list(path_visit(start='start',
                            end='end',
                            system=system,
                            gen_node=successors_v2))
    return len(paths)


if __name__ == '__main__':
    data = parse_data(day=12, parser=lambda x: x.split('-'))
    print(day12_1(data))
    print(day12_2(data))
