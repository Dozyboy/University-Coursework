# categories.py - Quan ly danh sach Loai hang va Don vi tinh
# Cho phep nguoi dung chon tu danh sach hoac them moi

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_CATEGORIES = os.path.join(BASE_DIR, "data", "categories.json")

# Gia tri mac dinh neu chua co file
DEFAULT_LOAI_HANG = [
    "Thuc pham",
    "Do uong",
    "Dien tu",
    "Van phong pham",
    "Tieu dung",
    "The thao",
    "Thoi trang",
    "Noi that",
    "Y te",
    "Khac"
]

DEFAULT_DON_VI_TINH = [
    "cai",
    "chiec",
    "doi",
    "hop",
    "tui",
    "thung",
    "chai",
    "lon",
    "kg",
    "g",
    "lit",
    "ml",
    "met",
    "ream",
    "vi"
]


# ============================================================
#  DOC / GHI FILE CATEGORIES
# ============================================================

def tai_categories():
    """Doc du lieu loai hang va don vi tinh tu file JSON."""
    if not os.path.exists(FILE_CATEGORIES):
        # Lan dau chay: tao file voi gia tri mac dinh
        du_lieu = {
            "loai_hang": DEFAULT_LOAI_HANG[:],
            "don_vi_tinh": DEFAULT_DON_VI_TINH[:]
        }
        _luu_categories(du_lieu)
        return du_lieu

    try:
        with open(FILE_CATEGORIES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return {
            "loai_hang": DEFAULT_LOAI_HANG[:],
            "don_vi_tinh": DEFAULT_DON_VI_TINH[:]
        }


def _luu_categories(du_lieu):
    """Ghi du lieu categories xuong file."""
    try:
        os.makedirs(os.path.dirname(FILE_CATEGORIES), exist_ok=True)
        with open(FILE_CATEGORIES, "w", encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"  [LOI] Khong the luu categories: {e}")
        return False


def them_loai_hang_moi(ten_loai):
    """Them mot loai hang moi vao danh sach."""
    du_lieu = tai_categories()
    # Kiem tra trung (khong phan biet hoa thuong)
    for loai in du_lieu["loai_hang"]:
        if loai.lower() == ten_loai.strip().lower():
            return False  # Da ton tai
    du_lieu["loai_hang"].append(ten_loai.strip())
    _luu_categories(du_lieu)
    return True


def them_don_vi_tinh_moi(don_vi):
    """Them mot don vi tinh moi vao danh sach."""
    du_lieu = tai_categories()
    for dvt in du_lieu["don_vi_tinh"]:
        if dvt.lower() == don_vi.strip().lower():
            return False  # Da ton tai
    du_lieu["don_vi_tinh"].append(don_vi.strip())
    _luu_categories(du_lieu)
    return True


# ============================================================
#  GIAO DIEN CHON TU DANH SACH
# ============================================================

def chon_loai_hang():
    """
    Hien thi danh sach loai hang, cho nguoi dung chon hoac them moi.
    Tra ve chuoi ten loai hang da chon.
    """
    return _chon_tu_danh_sach(
        tieu_de="CHON LOAI HANG",
        key="loai_hang",
        nhan_them="Them loai hang moi",
        ham_them=them_loai_hang_moi,
        nhan_nhap="  Nhap ten loai hang moi: "
    )


def chon_don_vi_tinh():
    """
    Hien thi danh sach don vi tinh, cho nguoi dung chon hoac them moi.
    Tra ve chuoi don vi tinh da chon.
    """
    return _chon_tu_danh_sach(
        tieu_de="CHON DON VI TINH",
        key="don_vi_tinh",
        nhan_them="Them don vi tinh moi",
        ham_them=them_don_vi_tinh_moi,
        nhan_nhap="  Nhap don vi tinh moi (VD: doi, thung, cuon): "
    )


def _chon_tu_danh_sach(tieu_de, key, nhan_them, ham_them, nhan_nhap):
    """
    Ham chung hien thi danh sach + cho chon + them moi.
    Tra ve gia tri da chon hoac None neu nguoi dung huy.
    """
    while True:
        du_lieu = tai_categories()
        danh_sach = du_lieu[key]

        print(f"\n  --- {tieu_de} ---")
        for i, item in enumerate(danh_sach):
            print(f"  {i + 1:>3}. {item}")
        print(f"  {'A':>3}. {nhan_them}")
        print(f"  {'0':>3}. Huy")
        print()

        lua_chon = input("  > Lua chon: ").strip().upper()

        if lua_chon == "0":
            return None

        if lua_chon == "A":
            gia_tri_moi = input(f"{nhan_nhap} (hoac 'q' de huy thao tac them): ").strip()
            
            if gia_tri_moi.lower() == 'q':
                continue # Quay lai menu chon
                
            # Lọc ký tự rác ngay tại đây (cấm các ký tự đặc biệt)
            for kt in ['"', "'", '*', '~', '`', '#', '$', '%', '^', '&', '\\', '|']:
                gia_tri_moi = gia_tri_moi.replace(kt, "")
            gia_tri_moi = " ".join(gia_tri_moi.split())
            
            if not gia_tri_moi:
                print("  [!] Ten khong duoc de trong hoac chi chua ky tu rac.")
                continue
                
            ket_qua = ham_them(gia_tri_moi)
            if ket_qua:
                print(f"  [OK] Da them '{gia_tri_moi}' vao danh sach.")
            else:
                print(f"  [!] '{gia_tri_moi}' da co trong danh sach roi.")
            # Quay lai hien thi de chon
            continue

        # Nguoi dung nhap so
        try:
            idx = int(lua_chon) - 1
            if 0 <= idx < len(danh_sach):
                return danh_sach[idx]
            else:
                print(f"  [!] Vui long chon so tu 1 den {len(danh_sach)}.")
        except ValueError:
            print("  [!] Lua chon khong hop le.")
