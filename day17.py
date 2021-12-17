from utils import parse_data
import re


def move_once(probe_loc, velocity):
    x, y = probe_loc
    dx, dy = velocity
    new_probe_loc = (x + dx, y + dy)
    if dx == 0:
        new_velocity_x = dx
    elif dx > 0:
        new_velocity_x = dx - 1
    else:
        new_velocity_x = dx + 1
    new_velocity = (new_velocity_x, dy - 1)
    return new_probe_loc, new_velocity


def simulate(x0, x1, y0, y1, velocity):
    probe_loc = (0, 0)
    path = []
    while True:
        probe_loc, velocity = move_once(probe_loc, velocity)
        path.append(probe_loc)
        x, y = probe_loc
        if x > x1 or y < y0:
            within_target = any(x0 <= x <= x1 and
                                y0 <= y <= y1
                                for x, y in path)
            return within_target, path


def solver(x0, x1, y0, y1):
    mem = {(x, y): simulate(x0, x1, y0, y1, (x, y))
           for x in range(-x1 - 1, x1 + 1)
           for y in range(y0 - 1, -y0 + 1)}
    return mem


def day17_1(x0, x1, y0, y1):
    mem = solver(x0, x1, y0, y1)
    mem = {k: max(elem[1] for elem in v[1])
           for k, v in mem.items()
           if v[0]}
    max_loc = max(mem, key=mem.get)
    return mem[max_loc]


def day17_2(x0, x1, y0, y1):
    mem = solver(x0, x1, y0, y1)
    mem = {k: v for k, v in mem.items() if v[0]}
    return len(mem.keys())


if __name__ == '__main__':
    data = parse_data(day=17,
                      parser=lambda x: re.findall(
                          r'.*?x=(\d+)..(\d+), y=-(\d+)..-(\d+)', x))
    x0, x1, y0, y1 = data[0][0]
    x0, x1, y0, y1 = int(x0), int(x1), -int(y0), -int(y1)
    print(day17_1(x0, x1, y0, y1))
    print(day17_2(x0, x1, y0, y1))
