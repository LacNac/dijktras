from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

def dijkstra_steps(n, edges, start, target):
    graph = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # đổi nếu muốn directed

    INF = float('inf')
    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)

    dist[start] = 0
    pq = [(0, start)]
    steps = []

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue

        steps.append({"type": "visit", "node": u})

        if u == target:
            break

        for v, w in graph[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

                steps.append({
                    "type": "relax",
                    "from": u,
                    "to": v,
                    "new_dist": dist[v]
                })

    path = []
    if dist[target] != INF:
        cur = target
        while cur != -1:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    return steps, dist[1:], path


@app.route("/")
def index():
    return render_template("index2.html")


@app.route("/run", methods=["POST"])
def run():
    data = request.json

    n = data["n"]
    start = data["start"]
    target = data["target"]
    edges = data["edges"]

    steps, dist, path = dijkstra_steps(n, edges, start, target)

    return jsonify({
        "steps": steps,
        "dist": dist,
        "path": path
    })


if __name__ == "__main__":
    app.run(debug=True)