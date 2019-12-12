import math


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def main():
    with open('input.txt', 'r') as f:
        moons = []
        for line in f.readlines():
            parts = line.split(',')
            x_str = parts[0][len('<x='):]
            y_str = parts[1][len(' y='):]
            z_str = parts[2][len(' z='):-2]
            pos = [int(x_str), int(y_str), int(z_str)]
            moons.append([pos, [0, 0, 0]])

    component_count = []

    for c in range(3):
        seen_states = set()
        counter = 0
        while True:
            state = (moons[0][0][c], moons[0][1][c], moons[1][0][c], moons[1][1][c], moons[2][0][c], moons[2][1][c], moons[3][0][c], moons[3][1][c])

            if state in seen_states:
                print("Done with", c)
                print(counter)
                component_count.append(counter)
                break

            seen_states.add(state)
            counter += 1
            for i, moon1 in enumerate(moons):
                for moon2 in moons[i+1:]:
                    if moon1[0][c] > moon2[0][c]:
                        moon1[1][c] -= 1
                        moon2[1][c] += 1
                    elif moon1[0][c] < moon2[0][c]:
                        moon1[1][c] += 1
                        moon2[1][c] -= 1

            for moon in moons:
                pos, vel = moon
                pos[c] += vel[c]
    print(lcm(lcm(component_count[0], component_count[1]), component_count[2]))


if __name__ == '__main__':
    main()
