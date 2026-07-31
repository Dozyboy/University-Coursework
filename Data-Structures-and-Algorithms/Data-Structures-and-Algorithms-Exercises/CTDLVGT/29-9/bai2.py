from __future__ import annotations
from fractions import Fraction
import math


# ----------------------------- INT EXAMPLES ---------------------------------
def int_examples(n: int = 10) -> dict:
	# Tổng 1..n (cách vòng lặp và công thức)
	total_loop = 0
	for i in range(1, n + 1):
		total_loop += i
	total_formula = n * (n + 1) // 2  # // là chia lấy phần nguyên

	# Giai thừa (factorial) đơn giản (cũng có math.factorial)
	fact = 1
	for i in range(2, n + 1):
		fact *= i
		
	return {
        'n': n, 
        'sum_loop': total_loop,
        'sum_formula': total_formula,
        'factorial': fact
    }


# ----------------------------- FLOAT EXAMPLES -------------------------------
def float_examples(values: list[float] | None = None) -> dict:
	if values is None:
		values = [1.2, 3.4, 5.6, 0.1]
	avg = sum(values) / len(values)
	sum_squares = sum(x * x for x in values)

	acc = 0.0
	for _ in range(10):  # cộng 0.1 mười lần
		acc += 0.1
	# Làm tròn (round(x, k) -> k chữ số thập phân)
	acc_rounded = round(acc, 10)

	print("[FLOAT]")
	print(f"  Danh sách        : {values}")
	print(f"  Trung bình       : {avg}")
	print(f"  Tổng bình phương : {sum_squares}")
	print(f"  Cộng 0.1 * 10    = {acc} (chưa làm tròn)")
	print(f"  Sau round(...,10): {acc_rounded}\n")

	return {
		'values': values,
		'average': avg,
		'sum_squares': sum_squares,
		'ten_times_point_one': acc,
		'ten_times_point_one_rounded': acc_rounded,
	}


# ----------------------------- BOOL EXAMPLES --------------------------------
def bool_examples(a: int = 5, b: int = 0) -> dict:
	comparisons = {
		'a > b': a > b,
		'a == b': a == b,
		'a != b': a != b,
		'b == 0': b == 0,
	}
	logic_ops = {
		'a>0 and b>0': (a > 0 and b > 0),
		'a>0 or  b>0': (a > 0 or b > 0),
		'not (b>0)': (not (b > 0)),
	}
	samples = [0, 1, -3, "", "hi", [], [1], None, True, False]
	truthiness = {repr(x): bool(x) for x in samples}

	print("[BOOL]")
	print("  So sánh:")
	for k, v in comparisons.items():
		print(f"    {k:<10} -> {v}")
	print("  Logic:")
	for k, v in logic_ops.items():
		print(f"    {k:<15} -> {v}")
	print("  Truthiness:")
	for k, v in truthiness.items():
		print(f"    {k:<8} -> {v}")
	print()

	return {
		'comparisons': comparisons,
		'logic': logic_ops,
		'truthiness': truthiness,
	}


# ----------------------------- COMPLEX EXAMPLES -----------------------------
def complex_examples(z1: complex = 2 + 3j, z2: complex = 1 - 4j) -> dict:
	add_ = z1 + z2
	mul_ = z1 * z2
	conj_z1 = z1.conjugate()
	mag_z1 = abs(z1)  # sqrt(a^2 + b^2)
	# Góc pha dùng math.atan2(imag, real)
	phase_z1 = math.atan2(z1.imag, z1.real)

	print("[COMPLEX]")
	print(f"  z1 = {z1}, z2 = {z2}")
	print(f"  z1 + z2 = {add_}")
	print(f"  z1 * z2 = {mul_}")
	print(f"  conj(z1) = {conj_z1}")
	print(f"  |z1| = {mag_z1}")
	print(f"  phase(z1) rad = {phase_z1}\n")

	return {
		'z1': z1,
		'z2': z2,
		'add': add_,
		'mul': mul_,
		'conjugate': conj_z1,
		'magnitude': mag_z1,
		'phase': phase_z1,
	}


# ----------------------------- FRACTION EXAMPLES ----------------------------
def fraction_examples(a_num: int = 1, a_den: int = 3, b_num: int = 2, b_den: int = 5) -> dict:
	A = Fraction(a_num, a_den)
	B = Fraction(b_num, b_den)
	sum_frac = A + B
	prod_frac = A * B
	float_equiv = float(A) + float(B)
	# Rút gọn tự động: Fraction(2,4) -> Fraction(1,2)

	print("[FRACTION]")
	print(f"  A = {A} (={float(A)})")
	print(f"  B = {B} (={float(B)})")
	print(f"  A + B      = {sum_frac} (float ~ {float_equiv})")
	print(f"  A * B      = {prod_frac} (float ~ {float(A)*float(B)})")
	print(f"  Phần thực float có thể lệch nhẹ so với Fraction chính xác.\n")

	return {
		'A': A,
		'B': B,
		'sum': sum_frac,
		'product': prod_frac,
		'float_sum': float_equiv,
	}


# ----------------------------- MAIN DEMO ------------------------------------
def main_demo():
	"""Chạy demo tất cả ví dụ."""
	int_examples(12)
	float_examples()
	bool_examples(5, 0)
	complex_examples()
	fraction_examples()


if __name__ == "__main__":  # chạy trực tiếp file mới demo
	main_demo()
