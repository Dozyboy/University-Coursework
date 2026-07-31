# Bài 2: Tìm hiểu các cấu trúc điều kiện trong Python
# Trình bày: if, if-else, if-elif-else, if lồng nhau, toán tử 3 ngôi, match-case (Python 3.10+)
# Mỗi cấu trúc kèm 1 ví dụ minh họa đơn giản.

print("== BÀI 2: CẤU TRÚC ĐIỀU KIỆN ==\n")

# 1) if (điều kiện đơn)
print("-- if")
tuoi = 20
if tuoi >= 18:
    print("Bạn là người trưởng thành.")

# 2) if-else
print("\n-- if-else")
diem = 4.8
if diem >= 4:
    print("Qua môn")
else:
    print("Trượt môn")

# 3) if-elif-else (nhiều nhánh)
print("\n-- if-elif-else")
diem_tb = 8.2
if diem_tb >= 8.5:
    hoc_luc = "Giỏi"
elif diem_tb >= 7.0:
    hoc_luc = "Khá"
elif diem_tb >= 5.0:
    hoc_luc = "Trung bình"
else:
    hoc_luc = "Yếu"
print(f"Điểm TB={diem_tb} -> Học lực: {hoc_luc}")

# 4) if lồng nhau
print("\n-- if lồng nhau")
co_cccd = True
so_tien = 90000
if co_cccd:
    if so_tien >= 100000:
        print("Có thể vào công viên giải trí VIP")
    else:
        print("Có CCCD nhưng không đủ tiền vé VIP")
else:
    print("Không có CCCD, không thể vào khu này")

# 5) Toán tử 3 ngôi (conditional expression)
print("\n-- toán tử 3 ngôi")
number = 7
chan_le = "chẵn" if number % 2 == 0 else "lẻ"
print(f"{number} là số {chan_le}")

# 6) match-case (Python 3.10+)
print("\n-- match-case")
thu = 3
match thu:
    case 1:
        ten_thu = "Thứ hai"
    case 2:
        ten_thu = "Thứ ba"
    case 3:
        ten_thu = "Thứ tư"
    case 4:
        ten_thu = "Thứ năm"
    case 5:
        ten_thu = "Thứ sáu"
    case 6:
        ten_thu = "Thứ bảy"
    case 7:
        ten_thu = "Chủ nhật"
    case _:
        ten_thu = "Không hợp lệ"
print(f"Mã {thu} -> {ten_thu}")

print("\n== KẾT THÚC BÀI 2 ==")
