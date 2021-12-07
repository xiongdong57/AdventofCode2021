from utils import parse_data
from utils import convert_to_int


def fuel_cost(seq, pos):
    return sum(abs(elem - pos) for elem in seq)


def day07_1(data):
    pos_min = min(data)
    pos_max = max(data)
    return min(fuel_cost(data, pos) for pos in range(pos_min, pos_max + 1))


def fuel_cost_v2(seq, pos):
    # basic math: 1 + 2 + ... + n = n(n+1)/2
    fuels = 0
    for elem in seq:
        distance = abs(elem - pos)
        fuels += int(distance * (distance + 1) / 2)
    return fuels


def day07_2(data):
    pos_min = min(data)
    pos_max = max(data)
    return min(fuel_cost_v2(data, pos) for pos in range(pos_min, pos_max + 1))


if __name__ == '__main__':
    data = parse_data(day=7, parser=lambda x: x.split(','))[0]
    data = convert_to_int(data)
    print(day07_1(data))
    print(day07_2(data))
