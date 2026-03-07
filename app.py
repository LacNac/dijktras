from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, end):
    n = len(grid)
    m = len(grid[0])

    pq = [(0, start)]
    g = {start: 0}
    parent = {}

    while pq:
        _, cur = heapq.heappop(pq)

        if cur == end:
            break

        for dx, dy in DIRS:
            nx, ny = cur[0]+dx, cur[1]+dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != 1:
                ng = g[cur] + 1
                if (nx, ny) not in g or ng < g[(nx, ny)]:
                    g[(nx, ny)] = ng
                    f = ng + heuristic((nx, ny), end)
                    heapq.heappush(pq, (f, (nx, ny)))
                    parent[(nx, ny)] = cur

    # truy vết
    path = []
    cur = end
    if cur in parent or cur == start:
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        path.append(start)
        path.reverse()

    return path


@app.route("/")
def index():
    return render_template("index1.html")


@app.route("/run", methods=["POST"])
def run():
    data = request.json
    grid = data["grid"]
    start = tuple(data["start"])
    end = tuple(data["end"])

    path = astar(grid, start, end)
    return jsonify({"path": path})


if __name__ == "__main__":
    app.run(debug=True)