# Dijkstra Visualizer Suite

Bộ repo này gồm 2 ứng dụng Flask để minh họa các bài toán đường đi ngắn nhất:

- Ứng dụng 1: Tìm đường trên lưới (grid) bằng Dijkstra và sinh Top-K đường đi ngắn nhất bằng Yen.
- Ứng dụng 2: Minh họa Dijkstra trên đồ thị trọng số tổng quát theo từng bước visit/relax.

Mục tiêu của repo là giúp học thuật toán một cách trực quan, có thể tương tác và xem kết quả ngay trên giao diện web.

## Mục lục

- [Tổng quan repo](#tổng-quan-repo)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Yêu cầu môi trường](#yêu-cầu-môi-trường)
- [Cách cài đặt và chạy](#cách-cài-đặt-và-chạy)
- [Ứng dụng 1: Grid Pathfinding (Dijkstra + Yen Top-K)](#ứng-dụng-1-grid-pathfinding-dijkstra--yen-top-k)
- [Ứng dụng 2: Graph Dijkstra Visualizer](#ứng-dụng-2-graph-dijkstra-visualizer)
- [API chi tiết](#api-chi-tiết)
- [Lưu ý và giới hạn](#lưu-ý-và-giới-hạn)
- [Hướng phát triển tiếp](#hướng-phát-triển-tiếp)

## Tổng quan repo

Repo có 2 backend Flask riêng:

1. `app.py`
	 - Render giao diện `templates/index1.html`.
	 - Cho phép vẽ map lưới, đặt Start/End, vẽ tường, random map.
	 - Backend tìm `Top-K` đường đi ngắn nhất:
		 - Đường ngắn nhất đầu tiên bằng Dijkstra trên grid 4 hướng.
		 - Các đường thay thế bằng Yen's K-shortest paths.

2. `app2.py`
	 - Render giao diện `templates/index2.html`.
	 - Cho phép nhập đồ thị trọng số (n, edges, start, target).
	 - Trả về log từng bước Dijkstra (`visit`, `relax`) để frontend animate.

## Cấu trúc thư mục

```text
dijktras/
|- app.py                  # Backend grid pathfinding + Top-K
|- app2.py                 # Backend dijkstra trên đồ thị tổng quát
|- README.md               # Tài liệu repo
|- templates/
|  |- index1.html          # UI grid pathfinding
|  |- index2.html          # UI graph visualizer
|- __pycache__/            # File bytecode Python
```

## Yêu cầu môi trường

- Python 3.9+ (khuyến nghị 3.10 trở lên).
- pip.
- Trình duyệt bất kỳ (Chrome/Edge/Firefox).

Thư viện cần thiết:

- `Flask`

## Cách cài đặt và chạy

### 1. Tạo và kích hoạt virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu gặp lỗi execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Cài thư viện

```powershell
pip install -r requirements.txt
```

### 3. Chạy ứng dụng

#### Cách A: Grid Pathfinding (mặc định)

```powershell
python app.py
```

Mở trình duyệt tại:

```text
http://127.0.0.1:5000/
```

#### Cách B: Graph Dijkstra Visualizer

```powershell
python app2.py
```

Mở trình duyệt tại:

```text
http://127.0.0.1:5000/
```

Lưu ý: Không chạy đồng thời cả 2 app trên cùng port 5000 vì sẽ bị xung đột.

## Ứng dụng 1: Grid Pathfinding (Dijkstra + Yen Top-K)

### File liên quan

- Backend: `app.py`
- Frontend: `templates/index1.html`

### Chức năng chính

- Vẽ tường bằng chuột (hỗ trợ kéo liên tục, nối đường vẽ theo line).
- Đặt `Start`, `End`, xóa ô (`Erase`).
- Random map theo `wall density`.
- Đổi kích thước lưới (`5` đến `80`, mặc định `25`).
- Tìm Top-K đường đi (`k` từ `1` đến `30`).
- Hiển thị:
	- Đường ngắn nhất (rank 1) màu xanh lá.
	- Các đường thay thế màu khác nhau.
	- Chú giải từng hạng và mô tả độ dài (số bước).
	- Giải thích chênh lệch so với đường ngắn nhất.

### Input/logic backend

- Grid là ma trận 2D:
	- `0` = ô trống
	- `1` = tường
- Di chuyển 4 hướng: lên, xuống, trái, phải.
- Mỗi cạnh có chi phí 1.
- Kiểm tra hợp lệ:
	- Grid không rỗng.
	- Start/End nằm trong biên.
	- Start/End không nằm trong tường.
- K được giới hạn trong [1, 30].

### Kết quả trả về

- `best_path`: đường tốt nhất.
- `alternative_paths`: danh sách đường thay thế.
- `paths`: danh sách có rank và cost.

## Ứng dụng 2: Graph Dijkstra Visualizer

### File liên quan

- Backend: `app2.py`
- Frontend: `templates/index2.html`

### Chức năng chính

- Nhập số đỉnh, start, target, tốc độ animate.
- Quản lý cạnh theo từng dòng `u, v, w` (thêm/xóa nhanh).
- Random đồ thị theo:
	- Số cạnh mong muốn.
	- Bậc tối đa mỗi đỉnh.
	- Khoảng trọng số min/max.
	- Tùy chọn ưu tiên liên thông.
- Kéo thả node trực tiếp trên canvas.
- Vẽ nhãn trọng số ngay trên mỗi cạnh.
- Animate từng bước Dijkstra:
	- `visit node`
	- `relax edge`
- Hiển thị:
	- Bảng khoảng cách đến từng đỉnh `d(i)`.
	- Đường đi ngắn nhất cuối cùng.
	- Giải thích tổng trọng số theo từng cạnh.

### Input/logic backend

- Đồ thị được xử lý dạng vô hướng (edge thêm 2 chiều).
- Không cho phép trọng số âm.
- Kiểm tra đầu vào ngay trên frontend:
	- `u`, `v` trong [1..n]
	- `u != v`
	- Có ít nhất 1 cạnh

### Kết quả trả về

- `steps`: danh sách sự kiện phục vụ animate.
- `dist`: khoảng cách từ start đến từng đỉnh.
- `path`: đường đi ngắn nhất start -> target.

## API chi tiết

### 1) API cho app.py

- Route: `POST /run`
- Content-Type: `application/json`

Request mẫu:

```json
{
	"grid": [[0,0,1],[0,0,0],[1,0,0]],
	"start": [0,0],
	"end": [2,2],
	"k": 5
}
```

Response thành công (ví dụ):

```json
{
	"best_path": [[0,0],[1,0],[1,1],[1,2],[2,2]],
	"alternative_paths": [
		[[0,0],[0,1],[1,1],[1,2],[2,2]]
	],
	"paths": [
		{"rank":1,"cost":4,"path":[[0,0],[1,0],[1,1],[1,2],[2,2]]},
		{"rank":2,"cost":4,"path":[[0,0],[0,1],[1,1],[1,2],[2,2]]}
	]
}
```

Response lỗi (400) có thể gặp:

- `Grid is empty`
- `Start or end is out of bounds`
- `Start or end cannot be inside a wall`

### 2) API cho app2.py

- Route: `POST /run`
- Content-Type: `application/json`

Request mẫu:

```json
{
	"n": 5,
	"start": 1,
	"target": 5,
	"edges": [
		[1,2,2],
		[1,3,4],
		[2,4,7],
		[3,5,1]
	]
}
```

Response thành công (ví dụ):

```json
{
	"steps": [
		{"type":"visit","node":1},
		{"type":"relax","from":1,"to":2,"new_dist":2}
	],
	"dist": [0,2,4,9,5],
	"path": [1,3,5]
}
```

## Lưu ý và giới hạn

- Cả 2 file backend đều dùng route gốc `/` và `/run`, mỗi lúc chỉ nên chạy 1 app.
- Thuật toán Dijkstra không hợp lệ với cạnh trọng số âm.
- Kích thước grid lớn (gần 80x80) và k cao có thể làm chậm phản hồi.
- Một số nội dung chữ trong frontend đang ở dạng không dấu; đây là vấn đề hiển thị, không ảnh hưởng tính đúng của thuật toán.

## Hướng phát triển tiếp

- Tách dependencies ra `requirements.txt`.
- Thêm test tự động cho:
	- Hàm tìm đường trên grid.
	- Hàm tạo steps Dijkstra trên đồ thị.
- Thêm tùy chọn đồ thị có hướng cho `app2.py`.
- Hỗ trợ đường chéo trên grid và tùy chọn heuristic (A*).
- Nhóm API sang blueprint riêng để dễ bảo trì.

---

Nếu bạn cần, mình có thể viết thêm `requirements.txt`, `run.bat` và cập nhật README theo hướng "1 lệnh là chạy" cho Windows.