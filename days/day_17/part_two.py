from collections import defaultdict, Counter
import math
import logging

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)


def get_turn_instruction(v_dir, path_dir):
    directions = ['U', 'R', 'D', 'L']
    v_i = directions.index(v_dir)
    path_i = directions.index(path_dir)
    if (v_i + 1) % 4 == path_i:
        return 'R'
    else:
        return 'L'

def main():
    with open('input.txt', 'r') as f:
        line = f.readline()
        program_line = [int(s) for s in line.strip().split(',')]
        program = defaultdict(int)
        for m, v in enumerate(program_line):
            program[m] = v

        orig_program = program.copy()

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

        vacuum_s = ord('^')
        vacuum = (-1,-1)

        scaffold_s = ord('#')
        poses = set()
        for y in range(len(rows)):
            for x in range(len(rows[y])):
                if rows[y][x] == scaffold_s:
                    poses.add((x,y))
                elif rows[y][x] == vacuum_s:
                    vacuum = (x,y)

        # move through the path
        cur_path_dir = None
        instructions = []

        cur_v_dir = 'U'

        vx, vy = vacuum
        if (vx, vy-1) in poses:
            cur_path_dir = 'U'
        if (vx, vy+1) in poses:
            cur_path_dir = 'D'
        if (vx -1, vy) in poses:
            cur_path_dir = 'L'
        if (vx+1, vy) in poses:
            cur_path_dir = 'R'

        if cur_v_dir != cur_path_dir:
            instructions.append(get_turn_instruction(cur_v_dir, cur_path_dir))


        while True:
            # if more path in cur path dir, move until the end
            cur_move = 0
            while True:
                vx, vy = vacuum
                print(vacuum, cur_path_dir)
                next_pos = None

                if cur_path_dir == 'U':
                    next_pos = (vx, vy - 1)
                if cur_path_dir == 'D':
                    next_pos = (vx, vy + 1)
                if cur_path_dir == 'L':
                    next_pos = (vx - 1, vy)
                if cur_path_dir == 'R':
                    next_pos = (vx + 1, vy)

                if next_pos in poses:
                    cur_move += 1
                    vacuum = next_pos
                else:
                    print("Can't go to", next_pos)
                    break

            print("moved", cur_move)
            instructions.append(cur_move)

            # turn the direction of the path and update cur path dir
            # if no more path, done

            if cur_path_dir == 'U':
                old_pos = (vx, vy + 1)
            if cur_path_dir == 'D':
                old_pos = (vx, vy - 1)
            if cur_path_dir == 'L':
                old_pos = (vx + 1, vy)
            if cur_path_dir == 'R':
                old_pos = (vx - 1, vy)

            neighbors = [n for n in [(vx, vy + 1),(vx, vy - 1),(vx + 1, vy),(vx - 1, vy)] if n in poses]
            print(cur_path_dir, neighbors, old_pos)

            neighbors.remove(old_pos)
            if not neighbors:
                break
            if len(neighbors) > 1:
                raise RuntimeError(neighbors)
            new_path_el = neighbors[0]

            if (vx, vy-1) == new_path_el:
                new_path_dir = 'U'
            if (vx, vy+1) == new_path_el:
                new_path_dir = 'D'
            if (vx -1, vy) == new_path_el:
                new_path_dir = 'L'
            if (vx+1, vy) == new_path_el:
                new_path_dir = 'R'

            instructions.append(get_turn_instruction(cur_path_dir, new_path_dir))
            print("turning", instructions[-1])
            cur_path_dir = new_path_dir

        print(instructions)


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
