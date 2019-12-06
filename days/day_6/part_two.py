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

        you_parents = get_parents(orbits, 'YOU')
        san_parents = get_parents(orbits, 'SAN')

        all_common_parents = set(you_parents.keys()).intersection(san_parents.keys())
        closest_common_parent = sorted((value, key) for key, value in you_parents.items() if key in all_common_parents)[0][1]

    print(you_parents[closest_common_parent] + san_parents[closest_common_parent] - 2)


def get_parents(orbits, cur_object):
    distances = {}
    distance = 0
    while cur_object in orbits:
        cur_object = orbits[cur_object]
        distance += 1
        distances[cur_object] = distance
    return distances


if __name__ == '__main__':
    main()
