from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def in_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


def edge_key(a, b):
    # Store undirected edge in canonical order for stable blocked-edge checks.
    return tuple(sorted((a, b)))


def dijkstra_path(grid, start, end, blocked_nodes=None, blocked_edges=None):
    n = len(grid)
    m = len(grid[0])

    blocked_nodes = blocked_nodes or set()
    blocked_edges = blocked_edges or set()

    if start in blocked_nodes or end in blocked_nodes:
        return []

    pq = []
    heapq.heappush(pq, (0, 0, start))
    dist = {start: 0}
    parent = {}
    push_id = 0

    while pq:
        cur_dist, _, cur = heapq.heappop(pq)

        if cur_dist != dist.get(cur):
            continue

        if cur == end:
            break

        for dx, dy in DIRS:
            nx, ny = cur[0]+dx, cur[1]+dy
            nxt = (nx, ny)
            if not in_bounds(nx, ny, n, m):
                continue
            if grid[nx][ny] == 1:
                continue
            if nxt in blocked_nodes:
                continue
            if edge_key(cur, nxt) in blocked_edges:
                continue

            cand = cur_dist + 1
            if cand < dist.get(nxt, float("inf")):
                dist[nxt] = cand
                parent[nxt] = cur
                push_id += 1
                heapq.heappush(pq, (cand, push_id, nxt))

    path = []
    cur = end
    if cur in parent or cur == start:
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        path.append(start)
        path.reverse()

    return path


def yen_k_shortest_paths(grid, start, end, k=10):
    first_path = dijkstra_path(grid, start, end)
    if not first_path:
        return []

    accepted = [first_path]
    accepted_set = {tuple(first_path)}

    candidates_heap = []
    candidates_set = set()
    candidate_id = 0

    for kth in range(1, k):
        prev_path = accepted[kth - 1]

        for i in range(len(prev_path) - 1):
            spur_node = prev_path[i]
            root_path = prev_path[:i + 1]

            blocked_nodes = set(root_path[:-1])
            blocked_edges = set()

            for chosen in accepted:
                if len(chosen) > i and chosen[:i + 1] == root_path:
                    blocked_edges.add(edge_key(chosen[i], chosen[i + 1]))

            spur_path = dijkstra_path(
                grid,
                spur_node,
                end,
                blocked_nodes=blocked_nodes,
                blocked_edges=blocked_edges
            )

            if not spur_path:
                continue

            total_path = root_path[:-1] + spur_path
            key = tuple(total_path)

            if key in accepted_set or key in candidates_set:
                continue

            cost = len(total_path) - 1
            candidate_id += 1
            heapq.heappush(candidates_heap, (cost, candidate_id, total_path))
            candidates_set.add(key)

        next_path = None
        while candidates_heap and next_path is None:
            _, _, candidate = heapq.heappop(candidates_heap)
            key = tuple(candidate)
            candidates_set.discard(key)
            if key not in accepted_set:
                next_path = candidate

        if next_path is None:
            break

        accepted.append(next_path)
        accepted_set.add(tuple(next_path))

    ranked = []
    for idx, path in enumerate(accepted, start=1):
        ranked.append({
            "rank": idx,
            "cost": len(path) - 1,
            "path": path
        })

    return ranked


@app.route("/")
def index():
    return render_template("index1.html")


@app.route("/run", methods=["POST"])
def run():
    data = request.json
    grid = data["grid"]
    start = tuple(data["start"])
    end = tuple(data["end"])
    k = int(data.get("k", 10))

    n = len(grid)
    m = len(grid[0]) if n else 0

    if not n or not m:
        return jsonify({"error": "Grid is empty"}), 400

    if not in_bounds(start[0], start[1], n, m) or not in_bounds(end[0], end[1], n, m):
        return jsonify({"error": "Start or end is out of bounds"}), 400

    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return jsonify({"error": "Start or end cannot be inside a wall"}), 400

    k = max(1, min(k, 30))
    ranked_paths = yen_k_shortest_paths(grid, start, end, k=k)

    if not ranked_paths:
        return jsonify({
            "best_path": [],
            "alternative_paths": [],
            "paths": []
        })

    best_path = ranked_paths[0]["path"]
    alternatives = [entry["path"] for entry in ranked_paths[1:]]

    return jsonify({
        "best_path": best_path,
        "alternative_paths": alternatives,
        "paths": ranked_paths
    })


if __name__ == "__main__":
    app.run(debug=True)