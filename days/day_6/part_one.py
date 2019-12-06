from collections import defaultdict


def main():
    orbits = {}
    all_objects = set()
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            orbited, orbiter = line.strip().split(')', 1)
            orbits[orbiter] = orbited
            all_objects.add(orbited)
            all_objects.add(orbiter)

        num_orbits = 0
        for object in all_objects:
            cur_object = object
            while cur_object in orbits:
                cur_object = orbits[cur_object]
                num_orbits += 1

    print(num_orbits)


if __name__ == '__main__':
    main()
