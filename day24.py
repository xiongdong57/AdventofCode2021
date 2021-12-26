from utils import parse_data
import z3


def solve(program):
    solver = z3.Optimize()
    digits = [z3.BitVec(f'd_{i}', 64) for i in range(14)]

    for d in digits:
        solver.add(d >= 1)
        solver.add(d <= 9)
        digit_input = iter(digits)

    zero, one = z3.BitVecVal(0, 64), z3.BitVecVal(1, 64)
    registers = {r: zero for r in 'wxyz'}

    for i, line in enumerate(program):
        vars = line.split()
        if 'inp' in line:
            registers[vars[-1]] = next(digit_input)
            continue
        operator, a, b = vars
        b = registers[b] if b in registers else int(b)
        c = z3.BitVec(f'v{i}', 64)
        if operator == 'add':
            solver.add(c == registers[a] + b)
        elif operator == 'mul':
            solver.add(c == registers[a] * b)
        elif operator == 'mod':
            solver.add(registers[a] >= 0)
            solver.add(b > 0)
            solver.add(c == registers[a] % b)
        elif operator == 'div':
            solver.add(b != 0)
            solver.add(c == registers[a] / b)
        elif operator == 'eql':
            solver.add(c == z3.If(registers[a] == b, one, zero))
        else:
            raise ValueError(f'Unknown operator: {operator}')
        registers[a] = c

    solver.add(registers['z'] == 0)

    for func in (solver.maximize, solver.minimize):
        solver.push()
        func(sum((10 ** i) * d for i, d in enumerate(digits[::-1])))
        solver.check()
        print(f'{func.__name__}')
        m = solver.model()
        print(''.join([str(m[d]) for d in digits]))
        solver.pop()


if __name__ == '__main__':
    data = parse_data(day=24, parser=str)
    solve(data)
