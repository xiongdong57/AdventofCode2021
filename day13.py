import re
from collections import defaultdict
from utils import parse_data


def gen_data():
    data = parse_data(day=13, parser=str, sep='\n\n')
    dots = [line.split(',') for line in data[0].split('\n')]
    folds = [re.findall(r'.*?(\w)=(\d+)', line)[0]
             for line in data[1].split('\n')]

    return dots, folds


def make_map(dots):
    system = defaultdict()
    for x, y in dots:
        system[(int(x), int(y))] = '#'
    return system


def update_dot(dota, dotb):
    return '#' if '#' in [dota, dotb] else '.'


def update_fold_system(system, axis, num):
    new_system = defaultdict()
    for (x, y), dot in system.items():
        if axis == 'x':
            if x <= num:
                new_system[(x, y)] = dot
            else:
                new_system[(2*num - x, y)] = update_dot(system[(x, y)], dot)
        if axis == 'y':
            if y <= num:
                new_system[(x, y)] = dot
            else:
                new_system[(x, 2*num - y)] = update_dot(system[(x, y)], dot)
    return new_system


def day13_1(dots, folds):
    system = make_map(dots)
    for axis, num in folds[:1]:
        system = update_fold_system(system, axis, int(num))
    return list(system.values()).count('#')


def print_map(system):
    x = max(system, key=lambda x: x[0])[0]
    y = max(system, key=lambda x: x[1])[1]
    for dy in range(y + 1):
        for dx in range(x + 1):
            print(system.get((dx, dy), ' '), end='')
        print()
    print()


def day13_2(dots, folds):
    system = make_map(dots)
    for axis, num in folds:
        system = update_fold_system(system, axis, int(num))
    # ZKAUCFUC
    print_map(system)


if __name__ == '__main__':
    dots, folds = gen_data()
    print(day13_1(dots, folds))
    print(day13_2(dots, folds))
