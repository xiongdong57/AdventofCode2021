from utils import parse_data
from collections import defaultdict


def is_lowest_adjacent(height_map, loc):
    x, y = loc
    height = height_map[loc]
    # only consider up, down, left and right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return all(height_map.get((x+dx, y+dy), 9) > height
               for dx, dy in directions)


def make_map(data):
    height_map = defaultdict(int)
    for row in range(len(data)):
        for col in range(len(data[row])):
            height_map[(row, col)] = int(data[row][col])
    return height_map


def day09_1(data):
    height_map = make_map(data)
    risk_level = 0
    for loc, height in height_map.items():
        if is_lowest_adjacent(height_map, loc):
            risk_level += height + 1
    return risk_level


def visit_basins(height_map, loc, visited=[]):
    # BFS
    visited.append(loc)
    x, y = loc
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        new_loc = (x+dx, y+dy)
        if (new_loc not in visited and
           new_loc in height_map and
           height_map.get(new_loc) < 9):
            visit_basins(height_map, new_loc, visited)
    return len(visited)


def day09_2(data):
    height_map = make_map(data)
    basins = []
    for loc in height_map.keys():
        if is_lowest_adjacent(height_map, loc):
            basins.append(visit_basins(height_map, loc, []))
    basins = sorted(basins, reverse=True)
    return basins[0] * basins[1] * basins[2]


if __name__ == '__main__':
    data = parse_data(day=9, parser=str)
    print(day09_1(data))
    print(day09_2(data))
