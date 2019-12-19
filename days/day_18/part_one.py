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

    print(dfs_keys(start, poses, doors, keys, rev_keys, []))


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


def dfs_keys(current_pos, poses, doors, keys, rev_keys, obtained_keys):
    print("starting from", obtained_keys)
    reachable_keys = can_reach_keys(current_pos, poses, doors, obtained_keys, keys)
    if not reachable_keys:
        return 0
    best_distance = 1000000
    for key in reachable_keys:
        # print("getting", key)
        key_pos = rev_keys[key]
        unlocked_doors = {pos for d, pos in doors.items() if d.lower() in obtained_keys}
        available_poses = poses.union(unlocked_doors)
        graph = make_graph(available_poses)
        distance = get_distance(current_pos, key_pos, graph) + dfs_keys(key_pos, poses, doors, keys, rev_keys, obtained_keys + [key])
        # print("got", key, "in", distance)
        if distance < best_distance:
            best_distance = distance
    if len(obtained_keys) == 10:
        print("best_distance", best_distance)
        raise RuntimeError
    return best_distance


def get_distance(p1, p2, graph):
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
        if u == p2:
            break
    return dist[p2]


if __name__ == '__main__':
    main()
