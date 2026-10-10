import numpy as np

# Bước 1: Tải dữ liệu viền ngoài từ file
outer_points = []
with open('visualize data/2310_outer_grid.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        x = float(parts[0].split(':')[1].strip())
        y = float(parts[1].split(':')[1].strip())
        z = float(parts[2].split(':')[1].strip())
        outer_points.append([x, y, z])

outer_points = np.array(outer_points)

# Bước 2: Xác định tọa độ viền ngoài
# Giả định các điểm nằm trên bốn cạnh của bảng
left_edge = outer_points[:18]           # Các điểm ở biên trái
right_edge = outer_points[-18:]          # Các điểm ở biên phải
top_edge = outer_points[18:42]           # Các điểm ở biên trên
bottom_edge = outer_points[42:60]        # Các điểm ở biên dưới

# Bước 3: Tạo lưới tọa độ cho 432 điểm (18 hàng x 24 cột)
num_rows = 18
num_cols = 24
grid_points = []

for i in range(num_rows):
    row_points = []
    for j in range(num_cols):
        # Tính toán tọa độ X và Y cho mỗi điểm
        x = left_edge[i][0] + (right_edge[i][0] - left_edge[i][0]) * j / (num_cols - 1)
        y = top_edge[j][1] + (bottom_edge[j][1] - top_edge[j][1]) * i / (num_rows - 1)
        z = (left_edge[i][2] + right_edge[i][2] + top_edge[j][2] + bottom_edge[j][2]) / 4  # Tính trung bình Z
        row_points.append([x, y, z])
    grid_points.append(row_points)

# Bước 4: Lưu các tọa độ vào file mới
with open('generated point/432_grid_points.txt', 'w') as f:
    for row in grid_points:
        for point in row:
            f.write(f"X: {point[0]:.2f}, Y: {point[1]:.2f}, Z: {point[2]:.2f}\n")

print("Tọa độ của 432 điểm đã được lưu vào file 432_grid_points.txt")