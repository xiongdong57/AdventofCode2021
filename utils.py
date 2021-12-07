from typing import List


def parse_data(day: int, parser=str, sep='\n'):
    with open(f'input/day{day:02d}.txt') as f:
        return [parser(line) for line in f.read().split(sep)]


def convert_to_int(data: List):
    return [int(elem) for elem in data]
