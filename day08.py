from utils import parse_data
from itertools import permutations


def gen_data():
    patterns = parse_data(day=8, parser=lambda x: x.split(' | ')[0])
    digits = parse_data(day=8, parser=lambda x: x.split(' | ')[1])
    patterns = [pattern.split() for pattern in patterns]
    digits = [digit.split() for digit in digits]
    return patterns, digits


def day08_1(patterns, digits):
    segments_map = {
        1: 2,
        4: 4,
        7: 3,
        8: 7
    }
    only_digits_counts = 0
    for line in digits:
        for digit in line:
            if len(digit) in segments_map.values():
                only_digits_counts += 1
    return only_digits_counts


def translate_to_chars(translator, chars: str):
    traslate_map = str.maketrans(''.join(translator), 'abcdefg')
    return chars.translate(traslate_map)


def translate_to_num(chars: str):
    char_to_num = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9'
    }
    key = ''.join(sorted(chars))
    return char_to_num.get(key, '')


def origin_chars_to_num(origin_chars, translator):
    chars = translate_to_chars(translator, origin_chars)
    return translate_to_num(chars)


def valid(pattern, translator):
    nums = [origin_chars_to_num(ch, translator) for ch in pattern]
    mark = ''.join(sorted(nums))
    return mark == '0123456789'


def solve_tranlator(pattern):
    # brute force, may be some clever dfs also can solve this
    for translator in permutations('abcdefg', 7):
        if valid(pattern, translator):
            return translator


def day08_2(patterns, digits):
    all_sum = 0
    for pattern, digit_nums in zip(patterns, digits):
        translator = solve_tranlator(pattern)
        num = ''
        for digit in digit_nums:
            num += origin_chars_to_num(digit, translator)
        all_sum += int(num)
    return all_sum


if __name__ == '__main__':
    patterns, digits = gen_data()
    print(day08_1(patterns, digits))
    print(day08_2(patterns, digits))
