from utils import parse_data
from collections import defaultdict


def make_map(data):
    energy_map = defaultdict(int)
    for row in range(len(data)):
        for col in range(len(data[row])):
            energy_map[(row, col)] = int(data[row][col])
    return energy_map


def get_neighbors(loc, energy_map):
    x, y = loc
    directions = [(0, 1), (1, 1), (1, 0), (1, -1),
                  (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    return [(x + dx, y + dy)
            for dx, dy in directions
            if (x + dx, y + dy) in energy_map]


def update_map(energy_map, flashed=[]):
    energy_map = energy_map.copy()
    for loc, energy in energy_map.items():
        if energy > 9 and loc not in flashed:
            for neighbor in get_neighbors(loc, energy_map):
                if neighbor not in flashed:
                    energy_map[neighbor] += 1
            flashed.append(loc)
    if all(eneryg <= 9 for loc, eneryg in energy_map.items()
       if loc not in flashed):
        return energy_map
    else:
        return update_map(energy_map, flashed)


def simulate(energy_map):
    flashes = 0
    energy_map = energy_map.copy()
    for loc, enery in energy_map.items():
        energy_map[loc] = enery + 1
    energy_map = update_map(energy_map, [])
    for loc, energy in energy_map.items():
        if energy > 9:
            energy_map[loc] = 0
            flashes += 1
    return flashes, energy_map


def print_map(energy_map):
    loc = list(energy_map.keys())[-1]
    x, y = loc
    for row in range(x + 1):
        for col in range(y + 1):
            print(energy_map[(row, col)], end='')
        print()
    print()


def day11_1(data):
    energy_map = make_map(data)
    all_flashes = 0
    for _ in range(100):
        flashes, energy_map = simulate(energy_map)
        all_flashes += flashes
    return all_flashes


def day11_2(data):
    energy_map = make_map(data)
    counter = 0
    while True:
        counter += 1
        _, energy_map = simulate(energy_map)
        if all(energy == 0 for energy in energy_map.values()):
            return counter


if __name__ == '__main__':
    data = parse_data(day=11, parser=str)
    print(day11_1(data))
    print(day11_2(data))
