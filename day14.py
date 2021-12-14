from utils import parse_data
from collections import defaultdict, Counter


def gen_data():
    pair_insertion_ruls = defaultdict()
    data = parse_data(day=14, sep='\n\n')
    template = data[0]
    for line in data[1].split('\n'):
        key, val = line.split(' -> ')
        pair_insertion_ruls[key] = val
    return template, pair_insertion_ruls


def simulate(template, pair_insertion_ruls):
    new_template = ''
    for i in range(len(template) - 1):
        left_char = template[i]
        right_char = template[i + 1]
        insert_char = pair_insertion_ruls[left_char + right_char]
        new_template += left_char + insert_char
    new_template += template[-1]
    return new_template


def day14_1(template, pair_insertion_ruls):
    for _ in range(10):
        template = simulate(template, pair_insertion_ruls)

    counter = Counter(template)
    most_common = counter.most_common(1)[0][1]
    least_common = counter.most_common()[-1][1]
    return most_common - least_common


def day14_2(template, pair_insertion_ruls):
    symbols_occurences = defaultdict(int)
    for x in template:
        symbols_occurences[x] += 1

    twograms_occurences = defaultdict(int)
    for i in range(len(template) - 1):
        x = template[i]
        y = template[i + 1]
        twograms_occurences[x + y] += 1

    for _ in range(40):
        new_insertions = []
        for pair, symbol in pair_insertion_ruls.items():
            if pair in twograms_occurences:
                new_insertions.append(
                    (pair, symbol, twograms_occurences[pair]))
                del twograms_occurences[pair]
        for pair, symbol, cnt in new_insertions:
            symbols_occurences[symbol] += cnt
            twograms_occurences[pair[0] + symbol] += cnt
            twograms_occurences[symbol + pair[1]] += cnt
    return max(symbols_occurences.values()) - min(symbols_occurences.values())


if __name__ == '__main__':
    template, pair_insertion_ruls = gen_data()
    print(day14_1(template, pair_insertion_ruls))
    print(day14_2(template, pair_insertion_ruls))
