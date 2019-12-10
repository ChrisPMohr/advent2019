from collections import defaultdict, Counter
from math import atan, pi


def computeGCD(x, y):
    while (y):
        x, y = y, x % y

    return x


def get_exact_angle(asteroid, other):
    delta_x = other[0] - asteroid[0]
    delta_y = other[1] - asteroid[1]
    if delta_x == 0 or delta_y == 0:
        num_steps = max(abs(delta_x), abs(delta_y))
    else:
        num_steps = computeGCD(abs(delta_x), abs(delta_y))
    delta_x //= num_steps
    delta_y //= num_steps
    return delta_x, delta_y


def angle(station, asteroid):
    delta_x = asteroid[0] - station[0]
    delta_y = asteroid[1] - station[1]
    if delta_x == 0:
        if delta_y > 0:
            return 3*pi/2
        else:
            return pi/2

    angle = atan(abs(delta_y/delta_x))
    if delta_x > 0:
        if delta_y > 0:
            return 2*pi - angle
        else:
            return angle
    else:
        if delta_y > 0:
            return pi + angle
        else:
            return pi - angle

def phase_shift(angle):
    shifted_angle = pi/2 - angle
    if shifted_angle < 0:
        return 2*pi + shifted_angle
    elif shifted_angle > 2*pi:
        return shifted_angle - 2*pi
    else:
        return shifted_angle


def get_sorted_asteroids(station, asteroids):
    return sorted(asteroids, key=lambda asteroid: phase_shift(angle(station, asteroid)))


def main():
    map = []
    asteroids = set()
    station = (29, 28)
    #station = (11,13)
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            map.append(list(line))
            for x, v in enumerate(line):
                if v == '#':
                    asteroids.add((x,y))
                if v == 'X':
                    station = (x,y)

        print(station)
        if station in asteroids:
            asteroids.remove(station)

        num_destroyed = 0
        while asteroids:
            sorted_asteroids = get_sorted_asteroids(station, asteroids)
            prev = sorted_asteroids.pop(0)
            last_batch = [prev]
            while sorted_asteroids:
                next = sorted_asteroids.pop(0)
                if get_exact_angle(station, prev) == get_exact_angle(station, next):
                    last_batch.append(next)
                else:
                    smallest_delta = 0
                    target = None
                    for asteroid in last_batch:
                        delta = abs(station[0] - asteroid[0])
                        if delta == 0:
                            delta = abs(station[1] - asteroid[1])
                        if target is None or delta < smallest_delta:
                            target = asteroid
                            smallest_delta = delta
                    num_destroyed += 1
                    print("Destroying", target, '-', num_destroyed, angle(station, target), phase_shift(angle(station, target)))
                    asteroids.remove(target)
                    last_batch = [next]
                prev = next


if __name__ == '__main__':
    main()
