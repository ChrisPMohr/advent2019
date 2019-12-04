def main():
    with open('input.txt', 'r') as f:
        wire_1_line = f.readline()
        wire_2_line = f.readline()
        wire_1_moves = parse_wire_moves(wire_1_line)
        wire_2_moves = parse_wire_moves(wire_2_line)
        wire_1_positions = set(get_move_positions(wire_1_moves))
        wire_2_positions = set(get_move_positions(wire_2_moves))
        intersections = wire_1_positions.intersection(wire_2_positions)
        best_distance = sorted(map(
            lambda coords: abs(coords[0]) + abs(coords[1]),
            intersections
        ))[0]

    print(best_distance)


def parse_wire_moves(line):
    move_strs = line.split(',')
    return [(move[0], int(move[1:])) for move in move_strs]


def get_move_positions(moves):
    x, y = 0, 0
    for direction, distance in moves:
        delta = (0, 0)
        if direction == 'L':
            delta = (-1, 0)
        if direction == 'R':
            delta = (1, 0)
        if direction == 'U':
            delta = (0, 1)
        if direction == 'D':
            delta = (0, -1)
        for i in range(distance):
            x += delta[0]
            y += delta[1]
            yield x, y


if __name__ == '__main__':
    main()
