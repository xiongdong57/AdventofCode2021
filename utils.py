from typing import List


def parse_data(day: int, parser=str, sep='\n'):
    with open(f'input/day{day:02d}.txt') as f:
        return [parser(line) for line in f.read().split(sep)]


def convert_to_int(data: List):
    return [int(elem) for elem in data]


def print_map(system, fillin='.'):
    # print the {(x, y): val} map
    x_max = max(system, key=lambda x: x[0])[0]
    x_min = min(system, key=lambda x: x[0])[0]
    y_max = max(system, key=lambda x: x[1])[1]
    y_min = min(system, key=lambda x: x[1])[1]
    for dy in range(y_min, y_max + 1):
        for dx in range(x_min, x_max + 1):
            print(system.get((dx, dy), fillin), end='')
        print()
    print()
