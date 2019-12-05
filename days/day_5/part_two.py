def main():
    pc = 0

    with open('input.txt', 'r') as f:
        line = f.readline()
        program = [int(s) for s in line.strip().split(',')]
        input = 5
        while True:
            orig_instruction = program[pc]
            instruction = orig_instruction % 100
            modes = ['0', '0', '0'] + list(str(int(orig_instruction // 100)))
            if instruction == 1:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                program[op3] = val1 + val2
                pc += 4
            elif instruction == 2:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                program[op3] = val1 * val2
                pc += 4
            elif instruction == 3:
                op1 = program[pc + 1]
                program[op1] = input
                pc += 2
            elif instruction == 4:
                op1 = program[pc + 1]
                val1 = program[op1] if modes[-1] == '0' else op1
                print("answer", val1)
                pc += 2
            elif instruction == 5:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                if val1 != 0:
                    pc = val2
                else:
                    pc += 3
            elif instruction == 6:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                if val1 == 0:
                    pc = val2
                else:
                    pc += 3
            elif instruction == 7:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                program[op3] = 1 if val1 < val2 else 0
                pc += 4
            elif instruction == 8:
                op1 = program[pc + 1]
                op2 = program[pc + 2]
                op3 = program[pc + 3]
                val1 = program[op1] if modes[-1] == '0' else op1
                val2 = program[op2] if modes[-2] == '0' else op2
                program[op3] = 1 if val1 == val2 else 0
                pc += 4
            elif instruction == 99:
                break
            else:
                raise RuntimeError("bad opcode " + str(instruction))


if __name__ == '__main__':
    main()
