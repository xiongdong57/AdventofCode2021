from utils import parse_data


def reduce_chunk(chunk: str):
    if any(ch in chunk for ch in ['()', '[]', '{}', '<>']):
        new_chunk = (chunk
                     .replace('()', '')
                     .replace('[]', '')
                     .replace('{}', '')
                     .replace('<>', ''))
        return reduce_chunk(new_chunk)
    else:
        return chunk


def day10_1(data):
    score = 0
    score_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
    for chunk in data:
        remain_chunk = reduce_chunk(chunk)
        corupted_chars = [ch
                          for ch in remain_chunk
                          if ch in [')', ']', '}', '>']]
        if corupted_chars:
            score += score_map[corupted_chars[0]]
    return score


def reverse_chunk(chunk):
    # reverse the incomplete chunk, will complete the chunk
    # such as: ([{{ and }}])
    new_chunk = chunk[::-1]
    chunk_map = {'(': ')', '[': ']', '{': '}', '<': '>'}
    return ''.join([chunk_map[ch] for ch in new_chunk])


def day10_2(data):
    scores = []
    score_map = {')': 1, ']': 2, '}': 3, '>': 4}
    for chunk in data:
        remain_chunk = reduce_chunk(chunk)
        corupted_chars = [ch
                          for ch in remain_chunk
                          if ch in [')', ']', '}', '>']]
        if not corupted_chars:
            score = 0
            for ch in reverse_chunk(remain_chunk):
                score = score * 5 + score_map[ch]
            scores.append(score)
    middle_index = int(len(scores) / 2)
    return sorted(scores)[middle_index]


if __name__ == '__main__':
    data = parse_data(day=10, parser=str)
    print(day10_1(data))
    print(day10_2(data))
