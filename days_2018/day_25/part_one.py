from collections import defaultdict
from operator import sub


def main():
    coordinates = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            coords = tuple(map(int, line.strip().split(',')))
            coordinates.append(coords)

    edges = defaultdict(list)
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            if is_adjacent(coordinates[i], coordinates[j]):
                edges[i].append(j)
                edges[j].append(i)

    components = find_connected_components(range(len(coordinates)), edges)
    print(len(components))


def man_dist(coord1, coord2):
    return sum(map(abs, map(sub, coord1, coord2)))


def is_adjacent(coord1, coord2):
    return man_dist(coord1, coord2) <= 3


def find_connected_components(coords, edges):
    visited = defaultdict(lambda: False)
    components = {}
    component_num = 1
    for coord in coords:
        if coord not in visited:
            component = bfs(coord, edges, visited)
            components[component_num] = component
            component_num += 1
    return components


def bfs(coord, edges, visited):
    if visited[coord]:
        return 0

    visited[coord] = True
    adjacent_coords = edges[coord]
    result = 1
    for adjacent_coord in adjacent_coords:
        result += bfs(adjacent_coord, edges, visited)
    return result


if __name__ == '__main__':
    main()
