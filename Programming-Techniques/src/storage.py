# storage.py - Doc ghi du lieu vao file JSON
# Su dung thu vien json va os (thu vien I/O tieu chuan, duoc phep dung)

import json
import os
from models import SanPham, GiaoDich

# Duong dan mac dinh den cac file du lieu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_SAN_PHAM = os.path.join(BASE_DIR, "data", "products.json")
FILE_GIAO_DICH = os.path.join(BASE_DIR, "data", "transactions.json")


# ===================== QUAN LY SAN PHAM =====================

def tai_danh_sach_san_pham():
    """
    Doc danh sach san pham tu file JSON.
    Tra ve danh sach (mang thu cong) cac doi tuong SanPham.
    """
    if not os.path.exists(FILE_SAN_PHAM):
        return []

    try:
        with open(FILE_SAN_PHAM, "r", encoding="utf-8") as f:
            du_lieu = json.load(f)

        danh_sach = []
        for item in du_lieu:
            danh_sach.append(SanPham.from_dict(item))
        return danh_sach

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[LOI] Khong the doc file san pham: {e}")
        return []


def luu_danh_sach_san_pham(danh_sach_sp):
    """
    Ghi danh sach san pham vao file JSON.
    danh_sach_sp: mang cac doi tuong SanPham
    """
    try:
        os.makedirs(os.path.dirname(FILE_SAN_PHAM), exist_ok=True)
        du_lieu = []
        for sp in danh_sach_sp:
            du_lieu.append(sp.to_dict())

        with open(FILE_SAN_PHAM, "w", encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        return True

    except Exception as e:
        print(f"[LOI] Khong the luu file san pham: {e}")
        return False


# ===================== QUAN LY GIAO DICH =====================

def tai_danh_sach_giao_dich():
    """
    Doc danh sach giao dich tu file JSON.
    Tra ve mang cac doi tuong GiaoDich.
    """
    if not os.path.exists(FILE_GIAO_DICH):
        return []

    try:
        with open(FILE_GIAO_DICH, "r", encoding="utf-8") as f:
            du_lieu = json.load(f)

        danh_sach = []
        for item in du_lieu:
            danh_sach.append(GiaoDich.from_dict(item))
        return danh_sach

    except (json.JSONDecodeError, KeyError) as e:
        print(f"[LOI] Khong the doc file giao dich: {e}")
        return []


def luu_danh_sach_giao_dich(danh_sach_gd):
    """
    Ghi danh sach giao dich vao file JSON.
    danh_sach_gd: mang cac doi tuong GiaoDich
    """
    try:
        os.makedirs(os.path.dirname(FILE_GIAO_DICH), exist_ok=True)
        du_lieu = []
        for gd in danh_sach_gd:
            du_lieu.append(gd.to_dict())

        with open(FILE_GIAO_DICH, "w", encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        return True

    except Exception as e:
        print(f"[LOI] Khong the luu file giao dich: {e}")
        return False


def them_giao_dich(giao_dich_moi):
    """
    Them mot giao dich moi vao file (doc -> append -> ghi lai).
    """
    danh_sach = tai_danh_sach_giao_dich()
    danh_sach.append(giao_dich_moi)
    return luu_danh_sach_giao_dich(danh_sach)


# ===================== SINH MA TU DONG =====================

def sinh_ma_giao_dich():
    """
    Tu dong tao ma giao dich moi theo dang GD0001, GD0002, ...
    Lay so lon nhat hien co va cong them 1.
    """
    danh_sach = tai_danh_sach_giao_dich()
    if len(danh_sach) == 0:
        return "GD0001"

    # Tim so lon nhat trong cac ma giao dich hien co
    so_lon_nhat = 0
    for gd in danh_sach:
        ma = gd.ma_gd
        if ma.startswith("GD") and ma[2:].isdigit():
            so = int(ma[2:])
            if so > so_lon_nhat:
                so_lon_nhat = so

    return f"GD{so_lon_nhat + 1:04d}"


def kiem_tra_ma_sp_ton_tai(ma_sp, danh_sach_sp):
    """
    Kiem tra xem ma san pham co ton tai trong danh sach khong.
    Tra ve True neu ton tai, False neu khong.
    Tu cai dat - khong dung ham tim kiem co san.
    """
    for sp in danh_sach_sp:
        if sp.ma_sp == ma_sp:
            return True
    return False


def tim_san_pham_theo_ma(ma_sp, danh_sach_sp):
    """
    Tim va tra ve doi tuong SanPham theo ma.
    Tra ve None neu khong tim thay.
    """
    for sp in danh_sach_sp:
        if sp.ma_sp == ma_sp:
            return sp
    return None
