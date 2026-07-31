# main.py - Diem khoi dong chuong trinh Quan Ly Kho Hang
# Nhom G22 - Chu de 3: Quan Ly Kho Hang
# Ngon ngu: Python

import sys
import os

# Dam bao Python tim thay cac module trong cung thu muc src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inventory import (
    them_san_pham, sua_san_pham, xoa_san_pham,
    hien_thi_tat_ca_san_pham, nhap_kho, xuat_kho
)
from search import menu_tim_kiem
from report import bao_cao_theo_thang, thong_ke_gia_tri_ton_kho, kiem_ke_tong_hop


# ============================================================
#  CAC MENU CON
# ============================================================

def menu_danh_muc():
    """Menu quan ly danh muc san pham."""
    while True:
        print("\n========================================")
        print("   QUAN LY DANH MUC SAN PHAM")
        print("========================================")
        print("  1. Hien thi tat ca san pham")
        print("  2. Them san pham moi")
        print("  3. Sua thong tin san pham")
        print("  4. Xoa san pham")
        print("  0. Quay lai menu chinh")
        print("----------------------------------------")

        lua_chon = input("  > Lua chon cua ban: ").strip()

        if lua_chon == "1":
            hien_thi_tat_ca_san_pham()
        elif lua_chon == "2":
            them_san_pham()
        elif lua_chon == "3":
            sua_san_pham()
        elif lua_chon == "4":
            xoa_san_pham()
        elif lua_chon == "0":
            break
        else:
            print("  [!] Lua chon khong hop le. Vui long chon lai.")

        input("\n  Nhan Enter de tiep tuc...")


def menu_nhap_xuat():
    """Menu quan ly nhap kho va xuat kho."""
    while True:
        print("\n========================================")
        print("   QUAN LY NHAP / XUAT KHO")
        print("========================================")
        print("  1. Nhap kho (tang so luong ton)")
        print("  2. Xuat kho (giam so luong ton)")
        print("  0. Quay lai menu chinh")
        print("----------------------------------------")

        lua_chon = input("  > Lua chon cua ban: ").strip()

        if lua_chon == "1":
            nhap_kho()
        elif lua_chon == "2":
            xuat_kho()
        elif lua_chon == "0":
            break
        else:
            print("  [!] Lua chon khong hop le. Vui long chon lai.")

        input("\n  Nhan Enter de tiep tuc...")


def menu_bao_cao():
    """Menu bao cao va thong ke."""
    while True:
        print("\n========================================")
        print("   BAO CAO & THONG KE")
        print("========================================")
        print("  1. Nhat ky nhap/xuat kho theo thang")
        print("  2. Thong ke gia tri hang ton kho")
        print("  3. Kiem ke tong hop kho hang")
        print("  0. Quay lai menu chinh")
        print("----------------------------------------")

        lua_chon = input("  > Lua chon cua ban: ").strip()

        if lua_chon == "1":
            bao_cao_theo_thang()
        elif lua_chon == "2":
            thong_ke_gia_tri_ton_kho()
        elif lua_chon == "3":
            kiem_ke_tong_hop()
        elif lua_chon == "0":
            break
        else:
            print("  [!] Lua chon khong hop le. Vui long chon lai.")

        input("\n  Nhan Enter de tiep tuc...")


# ============================================================
#  MENU CHINH
# ============================================================

def hien_thi_menu_chinh():
    """Hien thi man hinh menu chinh."""
    print("\n" + "=" * 50)
    print("    HE THONG QUAN LY KHO HANG - NHOM G22")
    print("=" * 50)
    print("  1. Quan ly danh muc san pham")
    print("  2. Nhap kho / Xuat kho")
    print("  3. Tim kiem san pham")
    print("  4. Bao cao & Thong ke")
    print("  0. Thoat chuong trinh")
    print("-" * 50)


def chay_chuong_trinh():
    """Vong lap chinh cua chuong trinh."""
    print("\n" + "=" * 52)
    print("    Chao mung den voi He Thong Quan Ly Kho Hang!")
    print("=" * 52)
    print("  Nhom G22 | Chu de 3: Quan Ly Kho Hang")
    print("  " + "-" * 48)
    print("  Thanh vien nhom:")
    print("    1. Thieu Quang Minh    - MSSV: 20227025")
    print("    2. Le Thi Thu Hien     - MSSV: 20227109")
    print("    3. Nguyen Tuan Dung    - MSSV: 20227191")
    print("=" * 52)

    while True:
        hien_thi_menu_chinh()
        lua_chon = input("  > Lua chon cua ban: ").strip()

        if lua_chon == "1":
            menu_danh_muc()
        elif lua_chon == "2":
            menu_nhap_xuat()
        elif lua_chon == "3":
            menu_tim_kiem()
            input("\n  Nhan Enter de tiep tuc...")
        elif lua_chon == "4":
            menu_bao_cao()
        elif lua_chon == "0":
            print("\n  Cam on ban da su dung chuong trinh. Tam biet!\n")
            break
        else:
            print("  [!] Lua chon khong hop le. Vui long chon lai (0-4).")
            input("  Nhan Enter de tiep tuc...")


# ============================================================
#  DIEM KHOI DONG
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="He thong Quan ly Kho Hang Nhom G22")
    parser.add_argument("--console", action="store_true", help="Chay chuong trinh duoi dang console CLI thay vi GUI")
    args = parser.parse_args()

    if args.console:
        chay_chuong_trinh()
    else:
        try:
            from gui import start_gui
            start_gui()
        except Exception as e:
            print(f"\n[!] Khong the khoi chay Giao dien do hoa (GUI): {e}")
            print("    He thong tu dong chuyen sang Giao dien dong lenh (Console/CLI)...\n")
            chay_chuong_trinh()
