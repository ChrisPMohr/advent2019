from fractions import Fraction


def get_slope(asteroid1, asteroid2):
    delta_x = asteroid1[0] - asteroid2[0]
    delta_y = asteroid1[1] - asteroid2[1]
    if delta_x != 0:
        return Fraction(delta_y, delta_x), delta_x > 0
    elif delta_y > 0:
        return "+Inf"
    else:
        return "-Inf"


def main():
    asteroids = set()
    with open('input.txt', 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, v in enumerate(line):
                if v == '#':
                    asteroids.add((x, y))

        scores = sorted([
            (len(set(get_slope(asteroid, other) for other in asteroids if other != asteroid)), asteroid)
            for asteroid in asteroids
        ], reverse=True)

    print(scores[0])


if __name__ == '__main__':
    main()
