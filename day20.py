from utils import parse_data
from collections import defaultdict


def gen_data():
    data = parse_data(day=20, parser=str, sep='\n\n')
    algorithm = data[0].replace('\n', '')
    image = defaultdict()
    for y, line in enumerate(data[1].split('\n')):
        for x, char in enumerate(line):
            image[(x, y)] = char
    return algorithm, image


def nine_locs(x, y):
    return [(x-1, y-1), (x, y-1), (x+1, y-1),
            (x-1, y), (x, y), (x+1, y),
            (x-1, y+1), (x, y+1), (x+1, y+1)]


def translate(loc, image, algorithm, step):
    code = ''
    for nloc in nine_locs(*loc):
        if step % 2 == 0 and algorithm[0] == '#':
            if nloc in image:
                code += '1' if image.get(nloc) == '#' else '0'
            else:
                code += '1'
        else:
            code += '1' if image.get(nloc) == '#' else '0'
    index = int(code, 2)
    return algorithm[index]


def simulate(image, algorithm, step):
    new_image = defaultdict()
    locs_to_explore = set()
    for loc in image.keys():
        for near_loc in nine_locs(*loc):
            locs_to_explore.add(near_loc)
    for loc in locs_to_explore:
        new_image[loc] = translate(loc, image, algorithm, step)
    return new_image


def day20_1(algorithm, image):
    for step in range(1, 3):
        image = simulate(image, algorithm, step)
    return list(image.values()).count('#')


def day20_2(algorithm, image):
    for step in range(1, 51):
        image = simulate(image, algorithm, step)
    return list(image.values()).count('#')


if __name__ == '__main__':
    algorithm, image = gen_data()
    print(day20_1(algorithm, image))
    print(day20_2(algorithm, image))
