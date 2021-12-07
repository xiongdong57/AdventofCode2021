from collections import defaultdict
from typing import List
from utils import parse_data
from utils import convert_to_int


def simulate(states: List):
    new_gen_state = states.count(0) * [6, 8]
    updated_states = [elem - 1 for elem in states if elem != 0]
    return updated_states + new_gen_state


def simulate_2(state: defaultdict):
    new_state = defaultdict(int)
    for key, value in state.items():
        if key == 0:
            new_state[6] += value
            new_state[8] += value
        else:
            new_state[key - 1] += value
    return new_state


def day06_1(data):
    state = data[:]
    for _ in range(80):
        state = simulate(state)
    return len(state)


def day06_2(data):
    state = defaultdict(int)
    for elem in data:
        if elem not in state.keys():
            state[elem] = data.count(elem)
    for _ in range(256):
        state = simulate_2(state)
    return sum(state.values())


if __name__ == '__main__':
    data = parse_data(day=6, parser=lambda x: x.split(','))[0]
    data = convert_to_int(data)
    print(day06_1(data))
    print(day06_2(data))
