from typing import List
from utils import parse_data


def convert_to_int(data: List):
    return [int(elem) for elem in data]


def parse_input():
    data = parse_data(day=4, parser=str.splitlines, sep='\n\n')
    nums = convert_to_int(data[0][0].split(','))
    boards = [[convert_to_int(line.split()) for line in board]
              for board in data[1:]]
    return nums, boards


def board_marks_valid(board: List[List], marked_nums: set):
    cols = [set([row[i] for row in board])
            for i in range(len(board[0]))]
    rows = [set(row) for row in board]
    lines = cols + rows
    return any(line.issubset(marked_nums) for line in lines)


def day04_1(nums, boards):
    for i, num in enumerate(nums):
        for board in boards:
            marked_nums = set(nums[:i+1])
            if board_marks_valid(board, marked_nums):
                all_unmark_nums_sum = sum([elem
                                           for row in board
                                           for elem in row
                                           if elem not in marked_nums])
                return num * all_unmark_nums_sum


def day04_2(nums, boards):
    remain_boards = boards[:]
    for i, num in enumerate(nums):
        marked_nums = set(nums[:i+1])
        remain_boards = [board
                         for board in remain_boards
                         if not board_marks_valid(board, marked_nums)]
        if len(remain_boards) == 1:
            last_board = remain_boards[0]
        if len(remain_boards) == 0:
            all_unmark_nums_sum = sum([elem
                                       for row in last_board
                                       for elem in row
                                       if elem not in marked_nums])
            return num * all_unmark_nums_sum


if __name__ == '__main__':
    nums, boards = parse_input()
    print(day04_1(nums, boards))
    print(day04_2(nums, boards))
