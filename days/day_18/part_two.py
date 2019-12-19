from collections import defaultdict, Counter
import math
import string
import heapq

"""
changes: 4 current poses/key (and start poses)
reachable keys should return a list for each remote bot
"""

MAX = 100000


def can_reach_keys(current_poses, poses, doors, unlocked_keys, keys):
    unlocked_doors = {pos for d, pos in doors.items() if d.lower() in unlocked_keys}
    poses = poses.union(unlocked_doors)
    result = []
    for current_pos in current_poses:
        reached_keys = set()
        dfs(current_pos, poses, keys, set(), reached_keys)
        result.append(reached_keys.difference(unlocked_keys))
    return result


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
    starts = []
    with open('input_part_2.txt', 'r') as f:
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
                    starts.append(pos)
                    poses.add(pos)

    all_poses = poses.union(doors.values())
    graph = make_graph(all_poses)

    key_to_key_distances = {}
    for p1, k1 in keys.items():
        key_distances = get_distances(p1, graph)
        for p2, k2 in keys.items():
            if k1 != k2:
                distance = key_distances[p2]
                if distance != MAX:
                    key_to_key_distances[(k1, k2)] = distance
        for i, start in enumerate(starts):
            distance = key_distances[start]
            if distance != MAX:
                key_to_key_distances[(str(i), k1)] = distance

    for i, start in enumerate(starts):
        rev_keys[str(i)] = start
    print(bfs_keys([str(i) for i in range(len(starts))], key_to_key_distances, poses, doors, keys, rev_keys))
    print("DONE")


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


def bfs_keys(current_keys, key_to_key_distances, poses, doors, keys, rev_keys):
    state = (0, current_keys, [])
    q = []
    heapq.heappush(q, state)
    seen_states = set()

    biggest_seen = 0
    while q:
        distance_acc, current_keys, obtained_keys = heapq.heappop(q)

        if distance_acc > biggest_seen:
            print(distance_acc)
            biggest_seen = distance_acc

        state = (tuple(current_keys), tuple(sorted(obtained_keys)))
        if state in seen_states:
            # print("skipping seen state")
            continue
        seen_states.add(state)
        # print(distance_acc, current_key, obtained_keys)
        # print(" " * len(obtained_keys), "starting from", current_keys, "have:", obtained_keys)
        current_poses = [rev_keys[key] for key in current_keys]
        reachable_keys_lists = can_reach_keys(current_poses, poses, doors, obtained_keys, keys)
        if not any(reachable_keys_lists):
            return distance_acc
        for i, reachable_keys in enumerate(reachable_keys_lists):
            for key in reachable_keys:
                new_distance_acc = distance_acc + key_to_key_distances[(current_keys[i], key)]
                # print(" " * len(obtained_keys), "got", key, "in", new_distance_acc)
                new_current_keys = list(current_keys)
                new_current_keys[i] = key
                heapq.heappush(q, (new_distance_acc, new_current_keys, obtained_keys + [key]))


def get_distances(p1, graph):
    dist = {}
    previous = {}
    for pos in graph:
        dist[pos] = MAX
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
