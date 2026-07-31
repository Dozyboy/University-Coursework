# search.py - Tim kiem san pham va loc san pham sap het hang
# Tu cai dat thuat toan tim kiem tuyen tinh (linear search)
# Khong su dung ham tim kiem co san cua Python

from storage import tai_danh_sach_san_pham


# ============================================================
#  PHAN 1: CAC HAM TIM KIEM TU CAI DAT
# ============================================================

def _chuan_hoa(chuoi):
    """Chuyen chuoi ve chu thuong va bo khoang trang de so sanh."""
    return chuoi.strip().lower()


def tim_kiem_theo_ma(ma_sp, danh_sach):
    """
    Tim kiem tuyen tinh theo ma san pham (chinh xac tuyet doi).
    Tra ve doi tuong SanPham hoac None.
    """
    ma_can_tim = _chuan_hoa(ma_sp)
    for sp in danh_sach:
        if _chuan_hoa(sp.ma_sp) == ma_can_tim:
            return sp
    return None


def tim_kiem_theo_ten(tu_khoa, danh_sach):
    """
    Tim kiem tuyen tinh theo ten san pham (cho phep khop mot phan).
    Tra ve mang cac san pham khop.
    """
    tu_khoa_chuan = _chuan_hoa(tu_khoa)
    ket_qua = []
    for sp in danh_sach:
        if tu_khoa_chuan in _chuan_hoa(sp.ten_sp):
            ket_qua.append(sp)
    return ket_qua


def tim_kiem_theo_loai(loai_hang, danh_sach):
    """
    Tim kiem tuyen tinh theo loai hang (cho phep khop mot phan).
    Tra ve mang cac san pham cung loai.
    """
    loai_chuan = _chuan_hoa(loai_hang)
    ket_qua = []
    for sp in danh_sach:
        if loai_chuan in _chuan_hoa(sp.loai_hang):
            ket_qua.append(sp)
    return ket_qua


def loc_san_pham_sap_het_hang(danh_sach):
    """
    Loc ra cac san pham co so_luong_ton <= nguong_toi_thieu.
    Sau do sap xep tang dan theo so luong ton (bubble sort tu cai dat).
    Tra ve mang cac san pham sap het hang.
    """
    # Buoc 1: Loc
    sap_het = []
    for sp in danh_sach:
        if sp.sap_het_hang():
            sap_het.append(sp)

    # Buoc 2: Sap xep bubble sort tang dan theo so_luong_ton
    n = len(sap_het)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if sap_het[j].so_luong_ton > sap_het[j + 1].so_luong_ton:
                sap_het[j], sap_het[j + 1] = sap_het[j + 1], sap_het[j]

    return sap_het


def sap_xep_theo_ten(danh_sach):
    """
    Sap xep danh sach san pham theo ten (A-Z) bang bubble sort.
    Tra ve mang moi (ban sao) da duoc sap xep.
    """
    ket_qua = []
    for sp in danh_sach:
        ket_qua.append(sp)

    n = len(ket_qua)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if _chuan_hoa(ket_qua[j].ten_sp) > _chuan_hoa(ket_qua[j + 1].ten_sp):
                ket_qua[j], ket_qua[j + 1] = ket_qua[j + 1], ket_qua[j]
    return ket_qua


# ============================================================
#  PHAN 2: MENU TIM KIEM (goi tu main)
# ============================================================

def menu_tim_kiem():
    """Menu con cho phan tim kiem san pham."""
    while True:
        print("\n--- TIM KIEM SAN PHAM ---")
        print("  1. Tim theo ma san pham")
        print("  2. Tim theo ten san pham (tu khoa)")
        print("  3. Tim theo loai hang")
        print("  4. Liet ke san pham sap het hang")
        print("  0. Quay lai menu chinh")

        lua_chon = input("  Lua chon: ").strip()

        if lua_chon == "1":
            _giao_dien_tim_theo_ma()
        elif lua_chon == "2":
            _giao_dien_tim_theo_ten()
        elif lua_chon == "3":
            _giao_dien_tim_theo_loai()
        elif lua_chon == "4":
            _giao_dien_san_pham_sap_het()
        elif lua_chon == "0":
            break
        else:
            print("  [!] Lua chon khong hop le.")

def _giao_dien_tim_theo_ma():
    danh_sach = tai_danh_sach_san_pham()
    ma = input("  Nhap ma san pham can tim (hoac 'q' de huy): ").strip()
    
    if ma.lower() == 'q':
        return # Thoat ngay
        
    # Loc ky tu rac (nhay kep/nhay don) de so sanh chinh xac hon
    ma = ma.replace('"', '').replace("'", "")
    
    if not ma:
        print("  [!] Ma san pham khong duoc de trong.")
        return
        
    sp = tim_kiem_theo_ma(ma, danh_sach)
    if sp:
        print("\n  Ket qua:")
        _in_chi_tiet_san_pham(sp)
    else:
        print(f"  [!] Khong tim thay san pham co ma '{ma}'.")

def _giao_dien_tim_theo_ten():
    danh_sach = tai_danh_sach_san_pham()
    tu_khoa = input("  Nhap tu khoa ten san pham (hoac 'q' de huy): ").strip()
    
    if tu_khoa.lower() == 'q': return # Thoát ngay
    tu_khoa = tu_khoa.replace('"', '').replace("'", "")
    if not tu_khoa:
        print("  [!] Tu khoa khong duoc de trong.")
        return
    ket_qua = tim_kiem_theo_ten(tu_khoa, danh_sach)
    _in_ket_qua_tim_kiem(ket_qua, f"ten chua '{tu_khoa}'")


def _giao_dien_tim_theo_loai():
    danh_sach = tai_danh_sach_san_pham()
    loai = input("  Nhap loai hang can tim (hoac 'q' de huy): ").strip()
    
    if loai.lower() == 'q':
        return # Thoat ngay
        
    # Loc ky tu rac
    loai = loai.replace('"', '').replace("'", "")
    
    if not loai:
        print("  [!] Loai hang khong duoc de trong.")
        return
        
    ket_qua = tim_kiem_theo_loai(loai, danh_sach)
    _in_ket_qua_tim_kiem(ket_qua, f"loai hang '{loai}'")


def _giao_dien_san_pham_sap_het():
    danh_sach = tai_danh_sach_san_pham()
    sap_het = loc_san_pham_sap_het_hang(danh_sach)

    print("\n" + "=" * 75)
    print(f"{'CANH BAO: SAN PHAM SAP HET HANG':^75}")
    print("=" * 75)

    if not sap_het:
        print("  Tat ca san pham deu co ton kho on dinh. Khong co canh bao nao.")
    else:
        print(f"  {'Ma SP':<10} {'Ten san pham':<25} {'DVT':<8} {'Ton kho':>8} {'Nguong':>8}")
        print("-" * 75)
        for sp in sap_het:
            print(f"  {sp.ma_sp:<10} {sp.ten_sp:<25} {sp.don_vi_tinh:<8} "
                  f"{sp.so_luong_ton:>8} {sp.nguong_toi_thieu:>8}")
        print("=" * 75)
        print(f"  Tong: {len(sap_het)} san pham can nhap them hang!")


def _in_chi_tiet_san_pham(sp):
    """In thong tin chi tiet mot san pham."""
    print(f"\n  {'=' * 50}")
    print(f"  Ma SP         : {sp.ma_sp}")
    print(f"  Ten san pham  : {sp.ten_sp}")
    print(f"  Loai hang     : {sp.loai_hang}")
    print(f"  Don vi tinh   : {sp.don_vi_tinh}")
    print(f"  So luong ton  : {sp.so_luong_ton}")
    print(f"  Don gia       : {sp.don_gia:,.0f} VND")
    print(f"  Nguong toi min: {sp.nguong_toi_thieu}")
    print(f"  Gia tri ton   : {sp.thanh_tien():,.0f} VND")
    trang_thai = "SAP HET HANG [!]" if sp.sap_het_hang() else "On dinh"
    print(f"  Trang thai    : {trang_thai}")
    print(f"  {'=' * 50}")


def _in_ket_qua_tim_kiem(ket_qua, mo_ta):
    """In ket qua tim kiem dang bang."""
    print(f"\n  Tim thay {len(ket_qua)} san pham voi {mo_ta}:")
    if not ket_qua:
        return
    print(f"\n  {'Ma SP':<10} {'Ten san pham':<25} {'Loai hang':<18} {'DVT':<8} {'Ton kho':>8} {'Don gia':>14}")
    print("  " + "-" * 85)
    for sp in ket_qua:
        print(f"  {sp.ma_sp:<10} {sp.ten_sp:<25} {sp.loai_hang:<18} {sp.don_vi_tinh:<8} "
              f"{sp.so_luong_ton:>8} {sp.don_gia:>14,.0f}")
