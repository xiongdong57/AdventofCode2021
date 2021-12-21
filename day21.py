from itertools import product
from functools import lru_cache


def play_game(p_pos, p_score, dice_pos):
    move_pos = 0
    for i in range(3):
        if (dice_pos + i) <= 100:
            move_pos += (dice_pos + i)
        else:
            move_pos += (dice_pos + i) - 100

    if (p_pos + move_pos) % 10 == 0:
        p_pos = 10
    else:
        p_pos = (p_pos + move_pos) % 10

    p_score += p_pos
    dice_pos = dice_pos + 3 if (dice_pos + 3) <= 100 else dice_pos + 3 - 100

    return p_pos, p_score, dice_pos


def day21_1():
    p1_pos, p2_pos = (7, 1)
    p1_score, p2_score = 0, 0
    dice_pos, dice_rolls = 1, 0
    while True:
        p1_pos, p1_score, dice_pos = play_game(p1_pos, p1_score, dice_pos)
        dice_rolls += 3
        if p1_score >= 1000:
            return p2_score * dice_rolls

        p2_pos, p2_score, dice_pos = play_game(p2_pos, p2_score, dice_pos)
        dice_rolls += 3
        if p2_score >= 1000:
            return p1_score * dice_rolls


def play_once(p_score, p_pos, rolls):
    if (p_pos + sum(rolls)) % 10 == 0:
        p_pos = 10
    else:
        p_pos = (p_pos + sum(rolls)) % 10
    p_score += p_pos
    return p_pos, p_score


@lru_cache(maxsize=None)
def count_wins(current_player, p1_pos, p1_score, p2_pos, p2_score):
    if p1_score >= 21:
        return 1, 0
    if p2_score >= 21:
        return 0, 1

    wins = [0, 0]
    for rolls in product(range(1, 4), repeat=3):
        if current_player == 0:
            new_pos, new_score = play_once(p1_score, p1_pos, rolls)
            win0, win1 = count_wins(1, new_pos, new_score, p2_pos, p2_score)
        else:
            new_pos, new_score = play_once(p2_score, p2_pos, rolls)
            win0, win1 = count_wins(0, p1_pos, p1_score, new_pos, new_score)
        wins[0] += win0
        wins[1] += win1
    return wins


def day21_2():
    p1_pos, p2_pos = (7, 1)
    p1_score, p2_score = 0, 0
    wins = count_wins(0, p1_pos, p1_score, p2_pos, p2_score)
    return max(wins)


if __name__ == '__main__':
    print(day21_1())
    print(day21_2())
