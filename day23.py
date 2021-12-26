from utils import parse_data


def gen_data():
    data = parse_data(day=23)
    state = []
    state.append(data[1][1])
    for loc in range(1, 6):
        state.append(data[1][2 * loc])
    state.append(data[1][11])

    for row in range(4):
        for line in range(4):
            state.append(data[line+2][3+row*2])
    return state


def display(state):
    print('#############')
    print("#" + state[0] + '.'.join(state[1:6]) + state[6] + "#")
    for line in range(2):
        t = "###"
        for row in range(4):
            t += state[7 + row + line] + '#'
        t += '##'
        print(t)
    print('#############')


def gen_state(s, a, b):
    return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]


Homes = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
Costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def move_home(s, cost):
    global Homes
    global Costs
    for hp in range(7):
        if s[hp] == '.':
            continue
        i = hp
        a = s[i]
        r = Homes[a]
        ofs = 7 + r*4
        line = 3
        while line > 0 and s[ofs+line] == a:
            line -= 1
        if s[ofs+line] != '.':
            continue
        cb = (2+line)*Costs[a]
        # go right
        while i < r + 1 and s[i+1] == '.':
            cb += Costs[a]*2 if i > 0 else Costs[a]
            i += 1
        # go left
        while i > r + 2 and s[i-1] == '.':
            cb += Costs[a]*2 if i < 6 else Costs[a]
            i -= 1
        if i != r + 1 and i != r + 2:
            continue
        return move_home(gen_state(s, hp, ofs+line), cost + cb)
    return (s, cost)


def move_out(s):
    global Homes
    global Costs
    # First move everybody in, if possible
    valid = []
    # Then try to get out, if possible
    for row in range(4):
        ofs = 7 + row*4
        line = 0
        while line < 4 and s[ofs+line] == '.':
            line += 1
        if line == 4:
            continue
        a = s[ofs+line]
        if (row == Homes[a] and
           (line == 3 or
           all(s[i] == a for i in range(ofs + line + 1, ofs+4)))):
            continue
        rr = row + 2
        cb = Costs[a]*line
        while rr < 7 and s[rr] == '.':
            cb += 2*Costs[a] if rr < 6 else Costs[a]
            valid.append(move_home(gen_state(s, rr, ofs+line), cb))
            rr += 1
        ll = row + 1
        cb = Costs[a]*line
        while ll >= 0 and s[ll] == '.':
            cb += 2*Costs[a] if ll > 0 else Costs[a]
            valid.append(move_home(gen_state(s, ll, ofs+line), cb))
            ll -= 1
    return valid


def search(start):
    queue = []
    for _ in range(100000):
        queue.append([])
    queue[0].append(start)
    previous = {start: None}
    mind = {start: 0}
    for cost in range(50000):
        for state in queue[cost]:
            if mind[state] < cost:
                continue
            valid = move_out(state)
            if all(state[i] == "." for i in range(7)) and len(valid) == 0:
                paths = []
                while state:
                    paths.append(state)
                    state = previous[state]
                return cost, paths
            for (nstate, ncost) in valid:
                if nstate in mind and mind[nstate] <= cost+ncost:
                    continue
                previous[nstate] = state
                mind[nstate] = cost + ncost
                queue[cost + ncost].append(nstate)


def solver(data):
    cost, _ = search(''.join(data))
    return cost


if __name__ == '__main__':
    data = gen_data()
    print(solver(data))
