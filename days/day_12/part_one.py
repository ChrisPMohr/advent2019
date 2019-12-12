from collections import defaultdict, Counter


def main():
    result = None
    with open('input.txt', 'r') as f:
        moons = []
        for line in f.readlines():
            parts = line.split(',')
            x_str = parts[0][len('<x='):]
            y_str = parts[1][len(' y='):]
            z_str = parts[2][len(' z='):-2]
            pos = [int(x_str), int(y_str), int(z_str)]
            moons.append([pos, [0, 0, 0]])

    for _ in range(1000):
        for i, moon1 in enumerate(moons):
            for moon2 in moons[i+1:]:
                for j in range(3):
                    if moon1[0][j] > moon2[0][j]:
                        moon1[1][j] -= 1
                        moon2[1][j] += 1
                    elif moon1[0][j] < moon2[0][j]:
                        moon1[1][j] += 1
                        moon2[1][j] -= 1

        for moon in moons:
            pos, vel = moon
            for i, v in enumerate(vel):
                pos[i] += v

        #for pos, vel in moons:
            #print('<', pos, '> <', vel, '>')

        total = 0
        for pos, vel in moons:
            pe = abs(pos[0]) + abs(pos[1]) + abs(pos[2])
            ke = abs(vel[0]) + abs(vel[1]) + abs(vel[2])
            total_e = pe*ke
            total += total_e
        print(total)
    print(result)


if __name__ == '__main__':
    main()
