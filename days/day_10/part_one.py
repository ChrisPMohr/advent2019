from collections import defaultdict, Counter


def computeGCD(x, y):
    while (y):
        x, y = y, x % y

    return x

def main():
    map = []
    asteroids = set()
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            map.append(list(line))
            for x, v in enumerate(line):
                if v == '#':
                    asteroids.add((x,y))

        print(asteroids)

        best_asteroid = None
        best_seen = 0
        for asteroid in asteroids:
            print("-"*80)
            print("Station on", asteroid)
            seen = 0
            for other in asteroids:
                if other == asteroid:
                    continue
                delta_x = other[0] - asteroid[0]
                delta_y = other[1] - asteroid[1]
                if delta_x == 0 or delta_y == 0:
                    num_steps = max(abs(delta_x), abs(delta_y))
                else:
                    num_steps = computeGCD(abs(delta_x), abs(delta_y))
                delta_x //= num_steps
                delta_y //= num_steps
                print(num_steps, delta_y, delta_x)
                collision = False
                for step in range(1, num_steps):
                    view_pos = (asteroid[0] + delta_x*step, asteroid[1] + delta_y*step)
                    if view_pos in asteroids:
                        collision = True
                        break
                if not collision:
                    print("Can see", other)
                    seen += 1
                else:
                    print("Cannot see", other, "collided with", view_pos)

            if best_asteroid is None or seen > best_seen:
                best_asteroid = asteroid
                best_seen = seen

    print(best_asteroid, best_seen)


if __name__ == '__main__':
    main()
