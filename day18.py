import ast
import math
import re
import copy
from utils import parse_data
from itertools import combinations


def find_nest_loc(exp):
    depth = 0
    for i, char in enumerate(exp):
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1

        if depth == 5:
            break

    for j, char in enumerate(exp[i:]):
        if char == ']':
            break

    if depth == 5:
        return exp[i:i+j+1], exp[:i], exp[i+j+1:]
    else:
        return None, None, None


def explode(exp):
    def add_left(m):
        return str(int(m.group(0)) + left_num)

    def add_right(m):
        return str(int(m.group(0)) + right_num)

    exp = str(exp)
    exp_four_pair, left_exp, right_exp = find_nest_loc(exp)
    if not exp_four_pair:
        return exp

    left_num, right_num = ast.literal_eval(exp_four_pair)
    exp_left = re.sub(r"\d+(?=\D*$)", add_left, left_exp)
    exp_right = re.sub(r"\d+", add_right, right_exp, count=1)

    final_exp = exp_left + '0' + exp_right
    return ast.literal_eval(final_exp)


def split(exp):
    def subsplit(m):
        num = int(m.group(0))
        return f"[{math.floor(int(num) / 2)},{math.ceil(num / 2)}]"

    exp = str(exp)
    return ast.literal_eval(re.sub(r"\d{2}", subsplit, exp, count=1))


def add(a, b):
    return [a, b]


def reduce(exp):
    out = explode(exp)
    if str(out) == str(exp):
        out = split(exp)
    return out


def recusive_reduce(exp):
    next_iter = exp
    while True:
        next_iter = reduce(next_iter)
        if str(next_iter) == str(reduce(next_iter)):
            break
    return next_iter


def calc_magnitude(exp):
    def magnitude(m):
        a = ast.literal_eval(m.group(0))
        return str(a[0] * 3 + a[1] * 2)

    exp = str(exp)
    out = re.sub(r'\[\d+, \d+\]', magnitude, exp)
    return ast.literal_eval(out)


def recusive_magnitude(exp):
    next_iter = exp
    while True:
        next_iter = calc_magnitude(next_iter)
        if str(next_iter) == str(calc_magnitude(next_iter)):
            break
    return next_iter


def day18_1(data):
    data = copy.deepcopy(data)
    running = data.pop(0)
    while data:
        next_add = data.pop(0)
        running = add(running, next_add)
        running = recusive_reduce(running)
    return recusive_magnitude(running)


def day18_2(data):
    scores = []
    for elem in combinations(data, 2):
        left, right = elem
        score1 = recusive_magnitude(recusive_reduce(add(left, right)))
        score2 = recusive_magnitude(recusive_reduce(add(right, left)))
        scores.append(score1)
        scores.append(score2)
    return max(scores)


if __name__ == '__main__':
    data = parse_data(day=18, parser=lambda x: ast.literal_eval(x))
    print(day18_1(data))
    print(day18_2(data))
