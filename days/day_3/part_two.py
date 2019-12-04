def main():
    with open('input.txt', 'r') as f:
        wire_1_line = f.readline()
        wire_2_line = f.readline()
        wire_1_moves = parse_wire_moves(wire_1_line)
        wire_2_moves = parse_wire_moves(wire_2_line)
        wire_1_positions = make_dict(get_move_positions_and_dist(wire_1_moves))
        wire_2_positions = make_dict(get_move_positions_and_dist(wire_2_moves))
        intersections = set(wire_1_positions.keys()).intersection(wire_2_positions.keys())
        best_distance = sorted(map(
            lambda coords: wire_1_positions[coords] + wire_2_positions[coords],
            intersections
        ))[0]

    print(best_distance)


def make_dict(positions_and_dists):
    dist_by_position = {}
    for x, y, dist in positions_and_dists:
        if (x, y) not in dist_by_position:
            dist_by_position[(x,y)] = dist
    return dist_by_position


def parse_wire_moves(line):
    move_strs = line.split(',')
    return [(move[0], int(move[1:])) for move in move_strs]


def get_move_positions_and_dist(moves):
    x, y = 0, 0
    dist = 0
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
            dist += 1
            yield x, y, dist


if __name__ == '__main__':
    main()
