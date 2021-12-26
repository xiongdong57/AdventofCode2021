from utils import parse_data
from collections import defaultdict


def gen_data():
    data = parse_data(day=25, parser=str)
    system = defaultdict()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            system[(x, y)] = c
    return system


def move_once(system):
    new_system = defaultdict()
    x_max, y_max = max(system)
    for loc, symbol in system.items():
        # move east-facing
        if loc in new_system:
            continue
        x, y = loc
        next_right_loc = (x + 1, y) if x < x_max else (0, y)
        if symbol == '>' and system[next_right_loc] == '.':
            new_system[next_right_loc] = '>'
            new_system[loc] = '.'
        else:
            new_system[loc] = symbol

    final_system = defaultdict()
    for loc, symbol in new_system.items():
        # move south-facing
        if loc in final_system:
            continue
        x, y = loc
        next_down_loc = (x, y + 1) if y < y_max else (x, 0)
        if symbol == 'v' and new_system[next_down_loc] == '.':
            final_system[next_down_loc] = 'v'
            final_system[loc] = '.'
        else:
            final_system[loc] = symbol

    return final_system


def day25(system):
    num = 0
    while True:
        num += 1
        new_system = move_once(system)
        if all(new_system[loc] == symbol for loc, symbol in system.items()):
            return num
        else:
            system = new_system


if __name__ == '__main__':
    system = gen_data()
    print(day25(system))
