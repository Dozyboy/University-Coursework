# Bài 1: Tìm hiểu các kiểu dữ liệu cơ bản trong Python
# Mỗi phần gồm: mô tả ngắn, ví dụ/bài toán minh họa, và in kết quả

print("== BÀI 1: CÁC KIỂU DỮ LIỆU CƠ BẢN ==\n")

# 1) int (số nguyên)
# Bài toán minh họa: cho 2 số nguyên a, b. Tính tổng, hiệu, tích, thương (nguyên), kiểm tra chẵn/lẻ của a
print("-- int (số nguyên)")
a, b = 17, 5
sum_ab = a + b
sub_ab = a - b
mul_ab = a * b
floordiv_ab = a // b  # chia lấy phần nguyên
is_a_even = (a % 2 == 0)
print(f"a={a}, b={b}; tổng={sum_ab}, hiệu={sub_ab}, tích={mul_ab}, chia_nguyên={floordiv_ab}, a_chẵn? {is_a_even}")

# 2) float (số thực)
# Bài toán minh họa: tính BMI = cân nặng(kg) / (chiều cao(m))^2 và phân loại xấp xỉ
print("\n-- float (số thực)")
can_nang = 58.0
chieu_cao = 1.65
bmi = can_nang / (chieu_cao ** 2)
print(f"BMI = {bmi:.2f}")

# 3) bool (đúng/sai)
# Bài toán: kiểm tra một học sinh có đủ điều kiện qua môn (điểm >= 5) không
print("\n-- bool (đúng/sai)")
diem = 6.25
qua_mon = diem >= 4
print(f"Điểm = {diem} -> Qua môn? {qua_mon}")

# 4) str (chuỗi)
# Bài toán: đếm số nguyên âm trong một chuỗi tiếng Việt không dấu
print("\n-- str (chuỗi)")
s = "lap trinh python co ban"
vowels = set("aeiou")
rev = s[::-1]
print(f"Chuỗi: '{s}', đảo chuỗi: '{rev}'")

# 5) list (danh sách, có thể thay đổi)
# Bài toán: cho danh sách điểm, tính trung bình, tìm min/max, sắp xếp
print("\n-- list (danh sách)")
diem_list = [7.5, 9.0, 6.0, 8.25, 5.5]
avg = sum(diem_list) / len(diem_list)
mi, ma = min(diem_list), max(diem_list)
sorted_asc = sorted(diem_list)
print(f"Điểm: {diem_list}, TB={avg:.2f}, min={mi}, max={ma}, tăng dần={sorted_asc}")

# 6) tuple (bộ, bất biến)
# Bài toán: lưu tọa độ 2D và tính khoảng cách Euclid giữa 2 điểm
print("\n-- tuple (bộ, bất biến)")
p1 = (2, 3)
p2 = (-1, 9)
dx, dy = p1[0] - p2[0], p1[1] - p2[1]
dist = (dx**2 + dy**2) ** 0.5
print(f"p1={p1}, p2={p2}, khoảng cách={dist:.3f}")

# 7) set (tập hợp, không phần tử trùng)
# Bài toán: loại bỏ phần tử trùng lặp, tính giao/hợp/hiệu của tập
print("\n-- set (tập hợp)")
A = set([1, 2, 2, 3, 4, 4, 5])  # -> {1,2,3,4,5}
B = {3, 4, 5, 6}
print(f"A={A}, B={B}, hợp={A|B}, giao={A&B}, hiệu A-B={A-B}")

# 8) dict (từ điển: key -> value)
# Bài toán: đếm tần suất ký tự trong chuỗi (bỏ khoảng trắng)
print("\n-- dict (từ điển)")
text = "google colab python"
freq = {}
for ch in text.replace(" ", ""):
    freq[ch] = freq.get(ch, 0) + 1
print(f"Chuỗi: '{text}', tần suất: {freq}")

# 9) complex (số phức)
# Bài toán: tính mô-đun (độ lớn) và tổng/nhân hai số phức
print("\n-- complex (số phức)")
z1 = 2 + 3j
z2 = 1 - 4j
z_sum = z1 + z2
z_mul = z1 * z2
z1_mod = abs(z1)
print(f"z1={z1}, z2={z2}, z1+z2={z_sum}, z1*z2={z_mul}, |z1|={z1_mod:.3f}")
