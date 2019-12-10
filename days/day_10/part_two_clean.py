from math import atan, pi


def get_angle(station, asteroid):
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
    else:
        return shifted_angle


def get_sorted_asteroids(station, asteroids):
    return sorted(asteroids, key=lambda asteroid: phase_shift(get_angle(station, asteroid)))


def main():
    asteroids = set()
    station = (29, 28)
    with open('input.txt', 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, v in enumerate(line):
                if v == '#':
                    asteroids.add((x, y))

        if station in asteroids:
            asteroids.remove(station)

        num_destroyed = 0
        while asteroids:
            sorted_asteroids = get_sorted_asteroids(station, asteroids)
            prev = sorted_asteroids.pop(0)
            last_batch = [prev]
            while sorted_asteroids:
                curr = sorted_asteroids.pop(0)
                if get_angle(station, prev) != get_angle(station, curr):
                    target = min(
                        last_batch,
                        key=lambda asteroid: (abs(station[0] - asteroid[0]), abs(station[0] - asteroid[0])))
                    num_destroyed += 1
                    if num_destroyed == 200:
                        print(target[0] * 100 + target[1])
                        return
                    asteroids.remove(target)
                    last_batch = []
                last_batch.append(curr)
                prev = curr


if __name__ == '__main__':
    main()
