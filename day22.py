from utils import parse_data
from collections import defaultdict
from itertools import product


def parse_line(line):
    def parse_loc(line):
        line_min, line_max = line[2:].split('..')
        return int(line_min), int(line_max)

    action, cubes = line.split(' ')
    x, y, z = cubes.split(',')
    x_min, x_max = parse_loc(x)
    y_min, y_max = parse_loc(y)
    z_min, z_max = parse_loc(z)
    return (action, x_min, x_max, y_min, y_max, z_min, z_max)


def day22_1(data):
    down_limit = -50
    up_limit = 50
    system = defaultdict()
    for line in data:
        action, x_min, x_max, y_min, y_max, z_min, z_max = line
        if (x_min >= up_limit or x_max <= down_limit or
           y_min >= up_limit or y_max <= down_limit or
           z_min >= up_limit or z_max <= down_limit):
            continue
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    system[(x, y, z)] = action
    return len([k for k, v in system.items() if v == 'on'])


def get_diff_cubes(cube_light, other_cub):
    x0, x1, y0, y1, z0, z1 = cube_light
    x3, x4, y3, y4, z3, z4 = other_cub
    if (x0 > x4 or x1 < x3 or y0 > y4 or y1 < y3 or z0 > z4 or z1 < z3):
        # no overlap
        return [(x0, x1, y0, y1, z0, z1)]
    sub_cubes = []
    left_x = (x0, max(x0, x3) - 1)
    mid_x = (max(x0, x3), min(x1, x4))
    right_x = (min(x1, x4) + 1, x1)

    left_y = (y0, max(y0, y3) - 1)
    mid_y = (max(y0, y3), min(y1, y4))
    right_y = (min(y1, y4) + 1, y1)

    left_z = (z0, max(z0, z3) - 1)
    mid_z = (max(z0, z3), min(z1, z4))
    right_z = (min(z1, z4) + 1, z1)

    for x, y, z in product([left_x, mid_x, right_x],
                           [left_y, mid_y, right_y],
                           [left_z, mid_z, right_z]):
        if x == mid_x and y == mid_y and z == mid_z:
            # skip middle cube(overlap with other cube)
            continue
        elif x[0] <= x[1] and y[0] <= y[1] and z[0] <= z[1]:
            # cube substracted
            # 3*9 - 1 = 26 sub cubes(except the most middle cube)
            sub_cubes.append((x[0], x[1], y[0], y[1], z[0], z[1]))

    return sub_cubes


def count_dots(cube):
    x_min, x_max, y_min, y_max, z_min, z_max = cube
    return (x_max - x_min + 1) * (y_max - y_min + 1) * (z_max - z_min + 1)


def day22_2(data):
    light_cubes = []
    for line in data:
        action, *cube = line
        new_cubes = []
        for cube_light in light_cubes:
            new_cubes += get_diff_cubes(cube_light, cube)
        light_cubes = new_cubes[:]
        if action == 'on':
            light_cubes.append(cube)
    return sum(count_dots(cube) for cube in light_cubes)


if __name__ == '__main__':
    data = parse_data(day=22, parser=parse_line)
    print(day22_1(data))
    print(day22_2(data))
