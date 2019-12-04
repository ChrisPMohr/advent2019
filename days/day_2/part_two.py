def main():
    for i in range(0,100):
        for j in range(0, 100):
            val = do_program(i, j)
            if val == 19690720:
                print(i, j)
                return


def do_program(input1, input2):
    pc = 0
    with open('input.txt', 'r') as f:
        line = f.readline()
        program = [int(s) for s in line.strip().split(',')]
        program[1] = input1
        program[2] = input2
        while True:
            instruction = program[pc]
            if instruction == 1:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1]
                val2 = program[op2]
                program[op3] = val1 + val2
            elif instruction == 2:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1]
                val2 = program[op2]
                program[op3] = val1 * val2
            elif instruction == 99:
                break
            else:
                raise RuntimeError("bad opcode " + str(instruction))
            pc += 4
    return program[0]


if __name__ == '__main__':
    main()
