import random

rows = 4          # số hàng
cols = 5          # số cột
min_val = 0       # giá trị nhỏ nhất
max_val = 100     # giá trị lớn nhất

matrix = []
for i in range(rows):
    row = []
    for j in range(cols):
        row.append(random.randint(min_val, max_val))
    matrix.append(row)

# In ma trận
print("Ma trận sinh ngẫu nhiên:")
for row in matrix:
    print(row)

print("Phần tử ở hàng 2, cột 3:", matrix[1][2])

new_row = [random.randint(min_val, max_val) for _ in range(cols)]
matrix.append(new_row)
print("\nSau khi thêm 1 hàng:")
for row in matrix:
    print(row)

# Thống kê đơn giản
all_numbers = []
for row in matrix:
    all_numbers.extend(row)

print("\nThống kê:")
print(" Số hàng:", len(matrix))
print(" Số cột (mỗi hàng):", cols)
print(" Số phần tử:", len(all_numbers))
print(" Giá trị nhỏ nhất:", min(all_numbers))
print(" Giá trị lớn nhất:", max(all_numbers))
print(" Tổng:", sum(all_numbers))