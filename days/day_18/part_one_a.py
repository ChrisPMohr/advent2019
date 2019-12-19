from collections import defaultdict, Counter
import math
import string


def can_reach_keys(start, poses, doors, unlocked_keys, keys):
    unlocked_doors = {pos for d, pos in doors.items() if d.lower() in unlocked_keys}
    poses = poses.union(unlocked_doors)
    reached_keys = set()
    dfs(start, poses, keys, set(), reached_keys)
    return reached_keys.difference(unlocked_keys)


def dfs(pos, poses, keys, seen, reached_keys):
    x,y = pos
    if pos in seen:
        return

    seen.add(pos)
    if pos in keys:
        reached_keys.add(keys[pos])

    for dx,dy in [(-1,0), (1,0), (0,1), (0,-1)]:
        nx, ny = x+dx, y+dy
        if (nx,ny) in poses:
            dfs((nx,ny), poses, keys, seen, reached_keys)


def main():
    poses = set()
    keys = {}
    rev_keys = {}
    doors = {}
    start = None
    with open('input1.txt', 'r') as f:
        lines = f.readlines()
        for y, line in enumerate(lines):
            for x, v in enumerate(line):
                pos = (x,y)
                if v == '.':
                    poses.add(pos)
                if v in string.ascii_lowercase:
                    keys[pos] = v
                    rev_keys[v] = pos
                    poses.add(pos)
                if v in string.ascii_uppercase:
                    doors[v] = pos
                if v == '@':
                    start = pos
                    poses.add(start)

    all_poses = poses.union(doors.values())
    graph = make_graph(all_poses)
    key_to_key_distances = {}
    for p1, k1 in keys.items():
        key_distances = get_distances(p1, graph)
        for p2, k2 in keys.items():
            if k1 != k2:
                distance = key_distances[p2]
                key_to_key_distances[(k1, k2)] = distance
        key_to_key_distances[(None, k1)] = key_distances[start]
    print(key_to_key_distances)

    rev_keys[None] = start
    print(dfs_keys(None, key_to_key_distances, poses, doors, keys, rev_keys, [], 0))


def make_graph(poses):
    graph = {}
    for x,y in poses:
        neighbors = []
        for dx,dy in [(-1,0), (1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if (nx,ny) in poses:
                neighbors.append((nx,ny))
        graph[(x,y)] = neighbors
    return graph


def dfs_keys(current_key, key_to_key_distances, poses, doors, keys, rev_keys, obtained_keys, distance_acc):
    print(" " * len(obtained_keys), "starting from", obtained_keys)
    current_pos = rev_keys[current_key]
    reachable_keys = can_reach_keys(current_pos, poses, doors, obtained_keys, keys)
    if not reachable_keys:
        return distance_acc
    best_distance = 1000000
    for key in reachable_keys:
        new_distance_acc = distance_acc + key_to_key_distances[(current_key, key)]
        total_distance = dfs_keys(key, key_to_key_distances, poses, doors, keys, rev_keys, obtained_keys + [key], new_distance_acc)
        print(" " * len(obtained_keys), "got", key, "in", total_distance)
        if total_distance < best_distance:
            best_distance = total_distance
    # if len(obtained_keys) == 5:
    #     print("best_distance", best_distance)
    #     raise RuntimeError
    return best_distance


def get_distances(p1, graph):
    dist = {}
    previous = {}
    for pos in graph:
        dist[pos] = 100000
        previous[pos] = None
    dist[p1] = 0
    q = list(graph.keys())
    while q:
        u = sorted(q, key=lambda p: dist[p])[0]
        q.remove(u)
        for neighbor in graph[u]:
            alt = dist[u] + 1
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                previous[neighbor] = u
    return dist


if __name__ == '__main__':
    main()
