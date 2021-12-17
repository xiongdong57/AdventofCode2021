from utils import parse_data
from functools import reduce


hex_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def parse_literals(bits):
    five_bits = bits[:5]
    if five_bits[0] == '0':
        return five_bits
    return five_bits + parse_literals(bits[5:])


def parse_packets(bits):
    version = int(bits[:3], 2)
    type_ID = int(bits[3:6], 2)
    if type_ID == 4:
        # literal value
        num_bits = parse_literals(bits[6:])
        num_filted = ''.join(num_bits[i]
                             for i in range(len(num_bits))
                             if i % 5 != 0)
        num = int(num_filted, 2)
        return {"version": version,
                "type_ID": type_ID,
                "literal": num,
                "sub-packets": None,
                "bits": bits[:6] + num_bits}
    else:
        # an operator
        bit_label = bits[6]
        if bit_label == '0':
            total_sub_length = int(bits[7:7+15], 2)
            sub_bits = bits[7+15:]
            occupy_bits = bits[:7+15]
            sub_packets = []
            while True:
                sub = parse_packets(sub_bits)
                sub_packets.append(sub)
                sub_bits = sub_bits[len(sub["bits"]):]
                occupy_bits += bits[len(occupy_bits):
                                    len(occupy_bits)+len(sub["bits"])]
                if (sum(len(sub["bits"]) for sub in sub_packets)
                   >= total_sub_length):
                    return {"version": version,
                            "type_ID": type_ID,
                            "operator": bit_label,
                            "sub-packets": sub_packets,
                            "bits": occupy_bits}
        elif bit_label == '1':
            num_sub_packets = int(bits[7:7+11], 2)
            sub_bits = bits[7+11:]
            occupy_bits = bits[:7+11]
            sub_packets = []
            for _ in range(num_sub_packets):
                sub = parse_packets(sub_bits)
                sub_packets.append(sub)
                sub_bits = sub_bits[len(sub["bits"]):]
                occupy_bits += bits[len(occupy_bits):
                                    len(occupy_bits)+len(sub["bits"])]
            return {"version": version,
                    "type_ID": type_ID,
                    "operator": bit_label,
                    "sub-packets": sub_packets,
                    "bits": occupy_bits}


def sum_version(packets):
    if not packets["sub-packets"]:
        return packets["version"]
    else:
        return packets["version"] + sum(sum_version(sub)
                                        for sub in packets["sub-packets"])


def day16_1(data):
    bits = ''.join(hex_map[elem] for elem in data[0])
    packets = parse_packets(bits)
    return sum_version(packets)


def evaluate(packets):
    if packets["type_ID"] == 4:
        return packets["literal"]
    elif packets["type_ID"] == 0:
        # sum
        return sum(evaluate(sub) for sub in packets["sub-packets"])
    elif packets["type_ID"] == 1:
        # product
        return reduce(lambda x, y: x*y,
                      [evaluate(sub) for sub in packets["sub-packets"]])
    elif packets["type_ID"] == 2:
        # min
        return min(evaluate(sub) for sub in packets["sub-packets"])
    elif packets["type_ID"] == 3:
        # max
        return max(evaluate(sub) for sub in packets["sub-packets"])
    elif packets["type_ID"] == 5:
        # greater than
        return (1
                if (evaluate(packets["sub-packets"][0]) >
                    evaluate(packets["sub-packets"][1]))
                else 0)
    elif packets["type_ID"] == 6:
        # less than
        return (1
                if (evaluate(packets["sub-packets"][0]) <
                    evaluate(packets["sub-packets"][1]))
                else 0)
    elif packets["type_ID"] == 7:
        # equal
        return (1
                if (evaluate(packets["sub-packets"][0]) ==
                    evaluate(packets["sub-packets"][1]))
                else 0)


def day16_2(data):
    bits = ''.join(hex_map[elem] for elem in data[0])
    packets = parse_packets(bits)
    return evaluate(packets)


if __name__ == '__main__':
    data = parse_data(day=16, parser=str)
    print(day16_1(data))
    print(day16_2(data))
