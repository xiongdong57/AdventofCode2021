from utils import parse_data
from itertools import combinations


class Scanner:
    def __init__(self, beacons) -> None:
        self.beacons = beacons
        self.final = set()
        self.offset = None

    def xy_rotation(self):
        yield lambda x, y, z: (x, y, z)
        yield lambda x, y, z: (y, -x, z)
        yield lambda x, y, z: (-x, -y, z)
        yield lambda x, y, z: (-y, x, z)

    def yz_rotation(self):
        yield lambda x, y, z: (x, y, z)
        yield lambda x, y, z: (x, z, -y)
        yield lambda x, y, z: (x, -y, -z)
        yield lambda x, y, z: (x, -z, y)

    def xz_rotation(self):
        yield lambda x, y, z: (x, y, z)
        yield lambda x, y, z: (z, y, -x)
        yield lambda x, y, z: (-x, y, -z)
        yield lambda x, y, z: (-z, y, x)

    def rotations(self):
        for xy in self.xy_rotation():
            for yz in self.yz_rotation():
                for xz in self.xz_rotation():
                    rotated_beacons = set()
                    for beacon in self.beacons:
                        rotated_beacons.add(xz(*yz(*xy(*beacon))))
                    yield rotated_beacons

    def translate(self, beacons, offset):
        return set([(beacon[0] + offset[0],
                    beacon[1] + offset[1],
                    beacon[2] + offset[2]) for beacon in beacons])


def solve(data):
    scanners = []
    for part in data:
        beacons = set()
        for line in part.split('\n'):
            if not line.startswith('--'):
                loc = [int(num) for num in line.split(',')]
                beacons.add(tuple(loc))
        scanners.append(Scanner(beacons))

    scanners[0].final = scanners[0].beacons
    scanners[0].offset = (0, 0, 0)

    fixed_scanner = set()
    fixed_scanner.add(scanners[0])

    while len(fixed_scanner) < len(scanners):
        for scanner in scanners:
            if scanner in fixed_scanner:
                continue

            fixed_beacons = set().union(*[s.final for s in fixed_scanner])
            for r in scanner.rotations():
                for floc in fixed_beacons:
                    for loc in r:
                        offset = (floc[0] - loc[0],
                                  floc[1] - loc[1],
                                  floc[2] - loc[2])
                        shifted = scanner.translate(r, offset)
                        if len(shifted.intersection(fixed_beacons)) >= 12:
                            scanner.final = shifted
                            scanner.offset = offset
                            fixed_scanner.add(scanner)
                            break
    return fixed_scanner, scanners


def day19_1(data):
    fixed_scanner, _ = solve(data)
    return len(set().union(*[s.final for s in fixed_scanner]))


def manhattan_distance(s1, s2):
    loc1 = s1.offset
    loc2 = s2.offset
    return (abs(loc1[0] - loc2[0]) +
            abs(loc1[1] - loc2[1]) +
            abs(loc1[2] - loc2[2]))


def day19_2(data):
    _, scanners = solve(data)
    return max(manhattan_distance(s1, s2)
               for s1, s2 in combinations(scanners, 2))


if __name__ == '__main__':
    data = parse_data(day=19, parser=str, sep='\n\n')
    print(day19_1(data))
    print(day19_2(data))
