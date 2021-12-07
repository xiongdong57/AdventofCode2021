for day in range(5, 26):
    with open(f'input/day{day:02d}.txt', 'w') as f:
        f.write('')
    with open(f'day{day:02d}.py', 'w') as f:
        f.write(f'''from utils import parse_data


def day{day:02d}_1(data):
    pass


def day{day:02d}_2(data):
    pass


if __name__ == '__main__':
    data = parse_data(day={day}, parser=str)
    print(day{day:02d}_1(data))
    print(day{day:02d}_2(data))
''')
