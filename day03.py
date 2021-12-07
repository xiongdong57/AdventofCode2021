from utils import parse_data


def common_bit(lst, descending=False):
    one_count = lst.count('1')
    zero_count = lst.count('0')
    if descending:
        return '1' if one_count >= zero_count else '0'
    else:
        return '0' if one_count >= zero_count else '1'


def day03_1(data):
    gamma_rate_str = ''
    epsilon_rate_str = ''
    for i in range(len(data[0])):
        bits = [elem[i] for elem in data]
        gamma_rate_str += common_bit(bits, descending=True)
        epsilon_rate_str += common_bit(bits, descending=False)

    return int(gamma_rate_str, 2) * int(epsilon_rate_str, 2)


def gen_bit_criteria(data, descending=True):
    filtered_data = data[:]
    for i in range(len(data[0])):
        bits = [elem[i] for elem in filtered_data]
        filter_bit = common_bit(bits, descending=descending)
        filtered_data = [
            elem for elem in filtered_data if elem[i] == filter_bit]
        if len(filtered_data) == 1:
            return filtered_data[0]


def day03_2(data):
    oxygen_generator_rate_str = gen_bit_criteria(data, descending=True)
    CO2_scrubber_rate_str = gen_bit_criteria(data, descending=False)
    return int(oxygen_generator_rate_str, 2) * int(CO2_scrubber_rate_str, 2)


if __name__ == '__main__':
    data = parse_data(day=3, parser=str)
    print(day03_1(data))
    print(day03_2(data))
