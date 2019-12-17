from collections import defaultdict, Counter
import math
import logging

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


def main():
    with open('input.txt', 'r') as f:
        line = f.readline()
        program_line = [int(s) for s in line.strip().split(',')]
        program = defaultdict(int)
        for m, v in enumerate(program_line):
            program[m] = v

        pc = 0
        relative_base = 0

        view = []

        while True:
            input_list = []
            output = run_program(program, input_list, pc, relative_base)
            if output is None:
                break
            else:
                val, program, pc, relative_base = output
                view.append(val)

        rows = []
        cur_row = []
        for v in view:
            if v == 10:
                rows.append(cur_row)
                cur_row = []
            else:
                cur_row.append(v)

        target = 35
        poses = set()
        for y in range(len(rows)):
            for x in range(len(rows[y])):
                if rows[y][x] == target:
                    poses.add((x,y))

        result = 0
        for p in poses:
            x,y = p
            if (x+1, y) in poses and (x-1, y) in poses and (x,y+1) in poses and (x,y-1) in poses:
                result += (x*y)

        print(result)
        print("\n".join([''.join([chr(v) for v in row]) for row in rows]))


def read_arg(arg_pos, is_address, instruction, program, pc, relative_base):
    op = program[pc + arg_pos]
    modes = ['0', '0', '0'] + list(str(int(instruction // 100)))
    mode = int(modes[-arg_pos])
    if is_address:
        if mode == 0:
            return op, op
        elif mode == 2:
            return op + relative_base, op
        else:
            raise ValueError("Illegal mode %s" % mode)
    else:
        if mode == 0:
            return program[op], op
        elif mode == 1:
            return op, op
        elif mode == 2:
            return program[op + relative_base], op
        else:
            raise ValueError("Illegal mode %s" % mode)


def run_program(program, input_stream, pc=0, relative_base=0):
    while True:
        orig_instruction = program[pc]
        instruction = orig_instruction % 100
        logger.debug("")
        logger.debug("%s - %s, relative base: %s", orig_instruction, instruction, relative_base)
        if instruction == 1:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            val3, op3 = read_arg(3, True, orig_instruction, program, pc, relative_base)
            logger.debug("add %s %s %s - %s + %s -> %s", op1, op2, op3, val1, val2, val3)
            program[val3] = val1 + val2
            pc += 4
        elif instruction == 2:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            val3, op3 = read_arg(3, True, orig_instruction, program, pc, relative_base)
            logger.debug("mult %s %s %s - %s * %s -> %s", op1, op2, op3, val1, val2, val3)
            program[val3] = val1 * val2
            pc += 4
        elif instruction == 3:
            val1, op1 = read_arg(1, True, orig_instruction, program, pc, relative_base)
            input = input_stream.pop()
            logger.debug("store %s - %s -> %s", op1, input, val1)
            program[val1] = input
            pc += 2
        elif instruction == 4:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            logger.debug("output %s - value: %s", op1, val1)
            pc += 2
            return val1, program, pc, relative_base
        elif instruction == 5:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            logger.debug("jmpnz %s %s - if %s != 0 jump %s", op1, op2, val1, val2)
            if val1 != 0:
                pc = val2
            else:
                pc += 3
        elif instruction == 6:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            logger.debug("jmpz %s %s - if %s == 0 jump %s", op1, op2, val1, val2)
            if val1 == 0:
                pc = val2
            else:
                pc += 3
        elif instruction == 7:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            val3, op3 = read_arg(3, True, orig_instruction, program, pc, relative_base)
            logger.debug("cmp %s %s %s - %s < %s -> %s", op1, op2, op3, val1, val2, val3)
            program[val3] = 1 if val1 < val2 else 0
            pc += 4
        elif instruction == 8:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            val2, op2 = read_arg(2, False, orig_instruction, program, pc, relative_base)
            val3, op3 = read_arg(3, True, orig_instruction, program, pc, relative_base)
            logger.debug("equal %s %s %s - %s == %s -> %s", op1, op2, op3, val1, val2, val3)
            program[val3] = 1 if val1 == val2 else 0
            pc += 4
        elif instruction == 9:
            val1, op1 = read_arg(1, False, orig_instruction, program, pc, relative_base)
            logger.debug("incr base %s - %s + %s -> %s", op1, relative_base, val1, relative_base + val1)
            relative_base += val1
            pc += 2
        elif instruction == 99:
            return None
        else:
            raise RuntimeError("bad opcode " + str(instruction))


if __name__ == '__main__':
    main()
