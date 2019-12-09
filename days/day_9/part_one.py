from itertools import permutations
from _collections import defaultdict


def main():
    with open('input.txt', 'r') as f:
        line = f.readline()
        program = [int(s) for s in line.strip().split(',')]
        output = run_program(program, [2,])
        for v in output:
            print("output", v)


def run_program(line, input_stream):
    pc = 0
    program = defaultdict(int)
    for m, v in enumerate(line):
        program[m] = v
    relative_base = 0
    while True:
        orig_instruction = program[pc]
        instruction = orig_instruction % 100
        #print("")
        #print(instruction, orig_instruction, 'relative base', relative_base)
        #print(program)
        modes = ['0', '0', '0'] + list(str(int(orig_instruction // 100)))
        if instruction == 1:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            op3 = program[pc + 3]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            val3 = op3 if modes[-3] == '0' else relative_base + op3
            #print("add", op1, op2, "-", val1, "+", val2, "to", op3)
            program[val3] = val1 + val2
            pc += 4
        elif instruction == 2:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            op3 = program[pc + 3]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            val3 = op3 if modes[-3] == '0' else relative_base + op3
            #print("mult", op1, op2, "-", val1, "*", val2, "to", op3)
            program[val3] = val1 * val2
            pc += 4
        elif instruction == 3:
            op1 = program[pc + 1]
            val1 = op1 if modes[-1] == '0' else relative_base + op1
            input = input_stream.pop()
            #print('store', op1, input, 'to', val1)
            program[val1] = input
            pc += 2
        elif instruction == 4:
            op1 = program[pc + 1]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            #print('output', op1, '- output value', val1)
            yield val1
            pc += 2
        elif instruction == 5:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            #print("cond jump", op1, op2, "if", val1, "jump", val2)
            if val1 != 0:
                pc = val2
            else:
                pc += 3
        elif instruction == 6:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            if val1 == 0:
                pc = val2
            else:
                pc += 3
        elif instruction == 7:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            op3 = program[pc + 3]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            val3 = op3 if modes[-3] == '0' else relative_base + op3
            #print("cmp", op1, op2, op3, val1, '<', val2, "to", op3, val1 < val2)
            program[val3] = 1 if val1 < val2 else 0
            pc += 4
        elif instruction == 8:
            op1 = program[pc + 1]
            op2 = program[pc + 2]
            op3 = program[pc + 3]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            val2 = program[op2] if modes[-2] == '0' else (program[relative_base + op2] if modes[-2] == '2' else op2)
            val3 = op3 if modes[-3] == '0' else relative_base + op3
            #print("equals", op1, op2, op3, val1, '=', val2, "to", op3, val1 == val2)
            program[val3] = 1 if val1 == val2 else 0
            pc += 4
        elif instruction == 9:
            op1 = program[pc + 1]
            val1 = program[op1] if modes[-1] == '0' else (program[relative_base + op1] if modes[-1] == '2' else op1)
            #print('incr base', op1, '- base incrd by', val1)
            relative_base += val1
            pc += 2
        elif instruction == 99:
            break
        else:
            raise RuntimeError("bad opcode " + str(instruction))


if __name__ == '__main__':
    main()
