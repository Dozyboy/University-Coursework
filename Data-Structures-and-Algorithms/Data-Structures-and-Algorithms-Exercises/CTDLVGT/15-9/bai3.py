# Bài 3: Triển khai Bài 1 và Bài 2 dưới dạng chương trình con (hàm)
# Cung cấp các hàm demo và một menu đơn giản để chạy từng phần.

from typing import List, Dict


def demo_kieu_du_lieu() -> None:
    print("== DEMO KIỂU DỮ LIỆU (Bài 1) ==\n")
    # int
    a, b = 17, 5
    print("[int]", {"a": a, "b": b, "tong": a + b, "hieu": a - b, "tich": a * b, "chia_nguyen": a // b})

    # float
    can_nang, chieu_cao = 58.0, 1.65
    bmi = can_nang / (chieu_cao ** 2)
    print("[float] BMI=", round(bmi, 2))

    # bool
    diem = 6.25
    print("[bool] qua_mon?", diem >= 4)

    # str
    s = "lap trinh python co ban"
    vowels = set("aeiou")
    print("[str] reverse=", s[::-1])

    # list
    diem_list = [7.5, 9.0, 6.0, 8.25, 5.5]
    print("[list] avg=", round(sum(diem_list) / len(diem_list), 2), 
          "; min=", min(diem_list), "; max=", max(diem_list))

    # tuple
    p1, p2 = (2, 3), (-1, 9)
    dx, dy = p1[0] - p2[0], p1[1] - p2[1]
    dist = (dx**2 + dy**2) ** 0.5
    print("[tuple] distance=", round(dist, 3))

    # set
    A, B = set([1, 2, 2, 3, 4, 4, 5]), {3, 4, 5, 6}
    print("[set] Hợp=", A | B, "; giao=", A & B, "; hiệu=", A - B)

    # dict
    text = "google colab python"
    freq: Dict[str, int] = {}
    for ch in text.replace(" ", ""):
        freq[ch] = freq.get(ch, 0) + 1
    print("[dict] freq=", freq)

    # complex
    z1, z2 = 2 + 3j, 1 - 4j
    print("[complex] sum=", z1 + z2, "; mul=", z1 * z2, "; |z1|=", round(abs(z1), 3))


def demo_dieu_kien() -> None:
    print("\n== DEMO CẤU TRÚC ĐIỀU KIỆN (Bài 2) ==\n")
    # if
    tuoi = 20
    if tuoi >= 18:
        print("[if] Trưởng thành")

    # if-else
    diem = 4.8
    print("[if-else]", "Qua" if diem >= 4 else "Trượt")

    # if-elif-else
    diem_tb = 8.2
    if diem_tb >= 8.5:
        hoc_luc = "Giỏi"
    elif diem_tb >= 7.0:
        hoc_luc = "Khá"
    elif diem_tb >= 5.0:
        hoc_luc = "Trung bình"
    else:
        hoc_luc = "Yếu"
    print("[if-elif-else] hoc_luc=", hoc_luc)

    # if lồng nhau
    co_cccd, so_tien = True, 90000
    if co_cccd:
        if so_tien >= 100000:
            print("[if lồng] Vào VIP")
        else:
            print("[if lồng] Có CCCD, thiếu tiền VIP")
    else:
        print("[if lồng] Không có CCCD")

    # toán tử 3 ngôi
    number = 7
    print("[3 ngôi]", "chẵn" if number % 2 == 0 else "lẻ")

    # match-case
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
    print("[match-case]", ten_thu)


def main():
    # Menu chạy nhanh các demo
    print("Chọn mục để chạy demo:")
    print("1. Demo kiểu dữ liệu (Bài 1)")
    print("2. Demo cấu trúc điều kiện (Bài 2)")
    print("3. Chạy cả hai")
    print("Khác: thoát")

    try:
        choice = input("Nhập lựa chọn (1/2/3): ").strip()
    except EOFError:
        choice = "3"  # nếu chạy trong môi trường không nhập được -> chạy cả hai

    if choice == "1":
        demo_kieu_du_lieu()
    elif choice == "2":
        demo_dieu_kien()
    elif choice == "3":
        demo_kieu_du_lieu()
        demo_dieu_kien()
    else:
        print("Thoát.")


if __name__ == "__main__":
    main()
