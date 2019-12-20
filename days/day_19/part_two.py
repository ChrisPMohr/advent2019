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

        biggest_x = []
        smallest_x = []

        size = 100

        y = 5
        while len(smallest_x) < 100 or biggest_x[-size] - smallest_x[-1] < size - 1:
            y += 1
            print(y)
            in_beam = False
            out_of_beam = False
            if smallest_x:
                x = smallest_x[-1] -1
            else:
                x = -1
            while True:
                x += 1
                curr_program = program.copy()
                pc = 0
                relative_base = 0
                input_list = [x, y]

                output = run_program(curr_program, input_list, pc, relative_base)
                if output is None:
                    break
                else:
                    val, _, _, _ = output
                    if val == 1:
                        if not in_beam:
                            smallest_x.append(x)
                            in_beam = True
                            print("in beam")
                            if len(biggest_x) > 5:
                                x = biggest_x[-1] - 1
                    else:
                        if in_beam:
                            biggest_x.append(x-1)
                            out_of_beam = True
                if out_of_beam:
                    print("breaking")
                    break

        print(smallest_x[-1] * 10000 + y-size+1)
        # print(biggest_x)
        # print(smallest_x)

        # print([y[0]-x[0] for x,y in zip(biggest_x, biggest_x[1:])])
        # print([y[0]-x[0] for x,y in zip(smallest_x, smallest_x[1:])])

        simul_small = [0,1,1,1,0,1,1]
        simul_big = [1,1,0,1,1,1,1,1,1]
        y = 8
        small_x = [6]
        big_x = [7]
        size = 100

        # simul_small = [0,1,1,1,1,1]
        # simul_big = [1,2,2,2,1,2,2]
        # y = 6
        # small_x = [6]
        # big_x = [10]
        # size = 10
        #
        # step = 0
        #
        # while step < size-1 or big_x[step-size+1] - small_x[step] < size - 1:
        #     small_x.append(small_x[-1] + simul_small[step%len(simul_small)])
        #     big_x.append(big_x[-1] + simul_big[step%len(simul_big)])
        #     step += 1
        #
        # print(small_x[step] * 10000 + step+y-size+1)




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
            input = input_stream.pop(0)
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
