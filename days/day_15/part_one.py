from _collections import defaultdict
import logging

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

directions = [1,2,3,4]

seen_positions = set()


def main():
    with open('input.txt', 'r') as f:
        line = f.readline()
        program_line = [int(s) for s in line.strip().split(',')]
        program = defaultdict(int)
        for m, v in enumerate(program_line):
            program[m] = v

        pc = 0
        relative_base = 0

        print(dfs((0,0), program, pc, relative_base))



def dfs(pos, orig_program, pc, relative_base):
    if pos in seen_positions:
        return None
    seen_positions.add(pos)
    print("visiting", pos)
    for direction in directions:
        program = orig_program.copy()
        output = run_program(program, [direction], pc, relative_base)
        if output is None:
            continue
        else:
            output_val, new_program, new_pc, new_relative_base = output
            if output_val == 2:
                return 1
            elif output_val == 1:
                print ("pos", pos, "safe to go", direction)
                if direction == 1:
                    new_pos = (pos[0], pos[1] + 1)
                elif direction == 2:
                    new_pos = (pos[0], pos[1] - 1)
                elif direction == 3:
                    new_pos = (pos[0] - 1, pos[1])
                elif direction == 4:
                    new_pos = (pos[0] + 1, pos[1])

                print("going to ", new_pos)

                ret = dfs(new_pos, new_program, new_pc, new_relative_base)
                if ret is not None:
                    return ret + 1


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
