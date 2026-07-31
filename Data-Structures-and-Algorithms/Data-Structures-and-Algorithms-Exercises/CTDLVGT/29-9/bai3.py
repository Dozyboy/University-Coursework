from fractions import Fraction


def int_demo(n):
	print("=== INT ===")
	# Tính tổng từ 1 đến n (dùng vòng lặp)
	tong = 0
	i = 1
	while i <= n:
		tong = tong + i
		i = i + 1
	print("Tổng 1..", n, "=", tong)

	# Giai thừa n (n!)
	gt = 1
	j = 1
	while j <= n:
		gt = gt * j
		j = j + 1
	print(n, "! =", gt)

	# Kiểm tra n có phải số chẵn
	if n % 2 == 0:
		print(n, "là số chẵn")
	else:
		print(n, "là số lẻ")
	print()


def float_demo():
	print("=== FLOAT ===")
	a = 0.1
	b = 0.2
	c = a + b
	print("a =", a, "b =", b, "a + b =", c)
	# So sánh với 0.3
	print("a + b == 0.3?", c == 0.3)  # Có thể False do sai số
	# Làm tròn
	print("round(a + b, 2) =", round(c, 2))
	print()


def bool_demo(x, y):
	print("=== BOOL ===")
	print("x =", x, "y =", y)
	print("x > y:", x > y)
	print("x == y:", x == y)
	print("x != y:", x != y)
	print("(x > 0) and (y > 0):", (x > 0) and (y > 0))
	print("(x > 0) or  (y > 0):", (x > 0) or (y > 0))
	print("not (y > 0):", not (y > 0))
	print()


def complex_demo():
	print("=== COMPLEX ===")
	z1 = 2 + 3j
	z2 = 1 - 4j
	print("z1 =", z1)
	print("z2 =", z2)
	print("z1 + z2 =", z1 + z2)
	print("z1 * z2 =", z1 * z2)
	print("Phần thực z1:", z1.real)
	print("Phần ảo  z1:", z1.imag)
	print()


def fraction_demo():
	print("=== FRACTION ===")
	# Tạo hai phân số 1/3 và 2/5
	f1 = Fraction(1, 3)
	f2 = Fraction(2, 5)
	print("f1 =", f1)
	print("f2 =", f2)
	print("f1 + f2 =", f1 + f2)
	print("f1 * f2 =", f1 * f2)
	# So sánh với float
	float_sum = float(f1) + float(f2)
	print("float(f1) + float(f2) =", float_sum)
	print()


def main():
	# Gọi các phần minh họa
	int_demo(5)       # có thể đổi số khác
	float_demo()
	bool_demo(5, 0)   # thử đổi giá trị
	complex_demo()
	fraction_demo()


if __name__ == "__main__":
	main()

# Gợi ý tự luyện:
# 1. Thêm vào int_demo: liệt kê tất cả ước của n.
# 2. Trong float_demo: thử cộng 0.1 nhiều lần (ví dụ 10 lần) rồi so sánh với 1.0.
# 3. Trong bool_demo: thêm ví dụ toán tử XOR (dùng != trên biểu thức True/False).
# 4. Trong complex_demo: in độ lớn (abs(z1)).
# 5. Trong fraction_demo: tính 1/1 + 1/2 + ... + 1/10 bằng Fraction.
