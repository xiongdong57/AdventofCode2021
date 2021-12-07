import re
from utils import parse_data
from collections import defaultdict


def gen_line_points(x1, y1, x2, y2, diagonal_line=False):
    points = []
    x_min = min(x1, x2)
    x_max = max(x1, x2)
    y_min = min(y1, y2)
    y_max = max(y1, y2)
    if x1 == x2:
        for y in range(y_min, y_max + 1):
            points.append((x1, y))
    elif y1 == y2:
        for x in range(x_min, x_max + 1):
            points.append((x, y1))
    elif diagonal_line:
        ascending = ((x1 == x_min and y1 == y_min) or
                     (x2 == x_min and y2 == y_min))
        for x in range(x_min, x_max + 1):
            if ascending:
                points.append((x, y_min + (x - x_min)))
            else:
                points.append((x, y_max - (x - x_min)))
    return points


def solve(data, diagnoal_line):
    picture = defaultdict(int)
    for line in data:
        x1, y1, x2, y2 = [int(elem) for elem in line]
        for point in gen_line_points(x1, y1, x2, y2,
                                     diagonal_line=diagnoal_line):
            picture[point] += 1
    return sum(1 for value in picture.values() if value > 1)


def day05_1(data):
    return solve(data, diagnoal_line=False)


def day05_2(data):
    return solve(data, diagnoal_line=True)


if __name__ == '__main__':
    data = parse_data(day=5,
                      parser=lambda x: re.findall(
                          r'(\d+),(\d+) -> (\d+),(\d+)', x)[0])
    print(day05_1(data))
    print(day05_2(data))
