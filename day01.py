from utils import parse_data


def day01_1(data):
    increase_count = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            increase_count += 1
    return increase_count


def day01_2(data):
    data_with_3_window = [sum(data[i:i+3]) for i in range(len(data) - 2)]
    return day01_1(data_with_3_window)


if __name__ == '__main__':
    data = parse_data(day=1, parser=int)
    print(day01_1(data))
    print(day01_2(data))
