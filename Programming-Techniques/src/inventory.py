# inventory.py - Nghiep vu quan ly Nhap kho / Xuat kho / Danh muc san pham
# Tu cai dat thuat toan, khong dung thu vien cau truc du lieu co san

import datetime
from models import SanPham, GiaoDich
from storage import (
    tai_danh_sach_san_pham, luu_danh_sach_san_pham,
    tai_danh_sach_giao_dich, them_giao_dich,
    kiem_tra_ma_sp_ton_tai, tim_san_pham_theo_ma, sinh_ma_giao_dich
)
from categories import chon_loai_hang, chon_don_vi_tinh


# ============================================================
#  TIEN ICH HIEN THI BANG SAN PHAM (dung chung)
# ============================================================

def _in_bang_san_pham(danh_sach, tieu_de="DANH SACH SAN PHAM"):
    """
    In bang danh sach san pham dang table co STT.
    Dung chung cho nhieu chuc nang: them, sua, xoa, nhap kho, xuat kho.
    """
    print("\n" + "=" * 95)
    print(f"  {tieu_de}")
    print("=" * 95)
    print(f"  {'STT':>4}  {'Ma SP':<10} {'Ten san pham':<24} {'Loai hang':<16} "
          f"{'DVT':<7} {'Ton kho':>8} {'Don gia':>13} {'Trang thai'}")
    print("  " + "-" * 91)
    for i, sp in enumerate(danh_sach):
        trang_thai = "[!] SAP HET" if sp.sap_het_hang() else ""
        print(f"  {i+1:>4}  {sp.ma_sp:<10} {sp.ten_sp:<24} {sp.loai_hang:<16} "
              f"{sp.don_vi_tinh:<7} {sp.so_luong_ton:>8} {sp.don_gia:>13,.0f} {trang_thai}")
    print("=" * 95)
    print(f"  Tong: {len(danh_sach)} san pham\n")


# ============================================================
#  PHAN 1: KIEM TRA TRUNG (tu cai dat, khong dung thu vien)
# ============================================================

def _kiem_tra_trung_ten(ten_moi, danh_sach, ma_bo_qua=None):
    """
    Kiem tra xem ten san pham co bi trung voi san pham nao khac khong.
    ma_bo_qua: bo qua san pham dang sua (khi edit).
    Tra ve doi tuong SanPham bi trung, hoac None neu khong trung.
    """
    ten_chuan = ten_moi.strip().lower()
    for sp in danh_sach:
        if ma_bo_qua and sp.ma_sp == ma_bo_qua:
            continue
        if sp.ten_sp.strip().lower() == ten_chuan:
            return sp
    return None


def _nhap_ten_san_pham(danh_sach, ma_bo_qua=None):
    """
    Nhac nhap ten san pham, kiem tra trung ten voi san pham khac.
    Hoi xac nhan neu trung, cho phep tiep tuc hoac nhap lai.
    Tra ve chuoi ten hop le.
    """
    while True:
        ten = input("  Ten san pham: ").strip()

        if ten.lower() == 'q':
            return None
            
        # Lam sach ky tu dac biet
        ten = _lam_sach_chuoi(ten)
        if not ten:
            print("  [!] Ten san pham khong duoc de trong.")
            continue

        trung = _kiem_tra_trung_ten(ten, danh_sach, ma_bo_qua)
        if trung:
            print(f"\n  [CANH BAO] Ten '{ten}' da ton tai:")
            print(f"  => Ma: {trung.ma_sp} | Loai: {trung.loai_hang} | "
                  f"Ton: {trung.so_luong_ton} {trung.don_vi_tinh}")
            xac_nhan = input("  Van muon dung ten nay? (y=tiep tuc / n=nhap lai): ").strip().lower()
            if xac_nhan == 'y':
                return ten
            # nguoi dung chon nhap lai -> vong lap tiep
            continue

        return ten


# ============================================================
#  PHAN 2: QUAN LY DANH MUC SAN PHAM
# ============================================================

def them_san_pham():
    """Them mot san pham moi vao danh muc. Nhap lieu tu ban phim."""
    print("\n--- THEM SAN PHAM MOI ---")
    danh_sach = tai_danh_sach_san_pham()

    # Liet ke san pham hien co de tranh nhap trung
    if danh_sach:
        _in_bang_san_pham(danh_sach, "SAN PHAM HIEN CO TRONG KHO (de tham khao)")
    else:
        print("  (Chua co san pham nao trong kho)\n")

    print("  --- NHAP THONG TIN SAN PHAM MOI ---")
    # --- Ma san pham ---
    while True:
        ma_sp = input("  Ma san pham (VD: SP011): ").strip().upper()
        if ma_sp.lower() == 'q':
            print("  Da huy them san pham.")
            return
        if not ma_sp:
            print("  [!] Ma san pham khong duoc de trong.")
            continue
        if kiem_tra_ma_sp_ton_tai(ma_sp, danh_sach):
            print(f"  [!] Ma '{ma_sp}' da ton tai. Vui long nhap ma khac.")
            continue
        break

    # --- Ten san pham (kiem tra trung) ---
    ten_sp = _nhap_ten_san_pham(danh_sach)
    if ten_sp is None:  # Bắt None ở đây
        print("  Da huy them san pham.")
        return

    # --- Loai hang (chon tu danh sach) ---
    print()
    loai_hang = chon_loai_hang()
    if loai_hang is None:
        print("  Da huy them san pham.")
        return

    # --- Don vi tinh (chon tu danh sach) ---
    print()
    don_vi_tinh = chon_don_vi_tinh()
    if don_vi_tinh is None:
        print("  Da huy them san pham.")
        return

    # --- So luong, gia, nguong ---
    so_luong_ton    = _nhap_so_nguyen_duong("  So luong ton kho ban dau")
    if so_luong_ton is None:  # Bắt None ở đây
        print("  Da huy them san pham.")
        return
    don_gia         = _nhap_so_thuc_duong("  Don gia (VND)")
    if don_gia is None:  # Bắt None ở đây
        print("  Da huy them san pham.")
        return
    nguong_toi_thieu = _nhap_so_nguyen_duong("  Nguong canh bao ton kho toi thieu")
    if nguong_toi_thieu is None:  
        print("  Da huy them san pham.")
        return

    sp_moi = SanPham(ma_sp, ten_sp, loai_hang, don_vi_tinh,
                     so_luong_ton, don_gia, nguong_toi_thieu)
    danh_sach.append(sp_moi)

    if luu_danh_sach_san_pham(danh_sach):
        print(f"\n  [OK] Da them san pham '{ten_sp}' ({ma_sp}) thanh cong!")
        print(f"       Loai: {loai_hang} | DVT: {don_vi_tinh} | "
              f"Ton kho: {so_luong_ton} | Don gia: {don_gia:,.0f} VND")
    else:
        print("  [LOI] Khong the luu san pham.")


def sua_san_pham():
    """Chinh sua thong tin mot san pham (tru ma SP)."""
    print("\n--- SUA THONG TIN SAN PHAM ---")
    danh_sach = tai_danh_sach_san_pham()
    if not danh_sach:
        print("  Khong co san pham nao trong kho.")
        return

    _in_bang_san_pham(danh_sach, "DANH SACH SAN PHAM - chon san pham can sua")

    ma_sp = _nhap_chuoi_an_toan("  Nhap ma san pham can sua")
    if ma_sp is None: 
        print("  Da huy thao tac sua san pham.")
        return
    ma_sp = ma_sp.upper()
    sp = tim_san_pham_theo_ma(ma_sp, danh_sach)
    if sp is None:
        print(f"  [!] Khong tim thay san pham co ma '{ma_sp}'.")
        return

    print(f"\n  --- THONG TIN HIEN TAI CUA SAN PHAM ---")
    print(f"  Ma SP         : {sp.ma_sp}")
    print(f"  Ten san pham  : {sp.ten_sp}")
    print(f"  Loai hang     : {sp.loai_hang}")
    print(f"  Don vi tinh   : {sp.don_vi_tinh}")
    print(f"  So luong ton  : {sp.so_luong_ton}")
    print(f"  Don gia       : {sp.don_gia:,.0f} VND")
    print(f"  Nguong toi min: {sp.nguong_toi_thieu}")
    print(f"  ----------------------------------------")
    print("  (Nhan Enter de giu nguyen gia tri cu, hoac 'q' de huy toan bo)\n")

    # --- Ten san pham ---
    ten_moi = input(f"  Ten san pham [{sp.ten_sp}]: ").strip()
    if ten_moi.lower() == 'q': return print("  Da huy thao tac sua.")
    if ten_moi:
        ten_moi = _lam_sach_chuoi(ten_moi) # Lọc ký tự rác
        trung = _kiem_tra_trung_ten(ten_moi, danh_sach, ma_bo_qua=ma_sp)
        if trung:
            print(f"\n  [CANH BAO] Ten '{ten_moi}' da ton tai o san pham khac:")
            print(f"  => Ma: {trung.ma_sp} | Loai: {trung.loai_hang}")
            xac_nhan = input("  Van muon dung ten nay? (y/n): ").strip().lower()
            if xac_nhan == 'y':
                sp.ten_sp = ten_moi
            else:
                print("  Giu nguyen ten cu.")
        else:
            sp.ten_sp = ten_moi

    # --- Loai hang ---
    doi_loai = input(f"  Doi loai hang [{sp.loai_hang}]? (y=doi, Enter=giu, q=huy): ").strip().lower()
    if doi_loai == 'q': return print("  Da huy thao tac sua.")
    if doi_loai == 'y':
        loai_moi = chon_loai_hang()
        if loai_moi is None: return print("  Da huy thao tac sua.") # Bắt None từ categories
        sp.loai_hang = loai_moi

    # --- Don vi tinh ---
    doi_dvt = input(f"  Doi don vi tinh [{sp.don_vi_tinh}]? (y=doi, Enter=giu, q=huy): ").strip().lower()
    if doi_dvt == 'q': return print("  Da huy thao tac sua.")
    if doi_dvt == 'y':
        dvt_moi = chon_don_vi_tinh()
        if dvt_moi is None: return print("  Da huy thao tac sua.") # Bắt None
        sp.don_vi_tinh = dvt_moi

    # --- Don gia ---
    gia_moi = input(f"  Don gia [{sp.don_gia:,.0f} VND]: ").strip()
    if gia_moi:
        try:
            gia = float(gia_moi.replace(",", ""))
            if gia <= 0:
                raise ValueError
            sp.don_gia = gia
        except ValueError:
            print("  [!] Gia tri khong hop le, giu nguyen don gia cu.")

    # --- Nguong toi thieu ---
    nguong_moi = input(f"  Nguong toi thieu [{sp.nguong_toi_thieu}] (Enter de giu, 'q' de huy): ").strip()
    if nguong_moi.lower() == 'q': return print("  Da huy thao tac sua.")
    if nguong_moi:
        try:
            n = int(nguong_moi)
            if n >= 0: sp.nguong_toi_thieu = n
        except ValueError:
            print("  [!] Gia tri khong hop le, giu nguyen nguong cu.")

    if luu_danh_sach_san_pham(danh_sach):
        print(f"\n  [OK] Da cap nhat san pham '{sp.ten_sp}' ({ma_sp}) thanh cong!")
    else:
        print("  [LOI] Khong the luu thay doi.")


def xoa_san_pham():
    """Xoa mot san pham khoi danh muc (chi xoa khi ton kho = 0)."""
    print("\n--- XOA SAN PHAM ---")
    danh_sach = tai_danh_sach_san_pham()
    if not danh_sach:
        print("  Khong co san pham nao trong kho.")
        return

    _in_bang_san_pham(danh_sach, "DANH SACH SAN PHAM - chon san pham can xoa")

    # Su dung ham an toan
    ma_sp = _nhap_chuoi_an_toan("  Nhap ma san pham can xoa")
    if ma_sp is None:
        print("  Da huy thao tac xoa san pham.")
        return
    ma_sp = ma_sp.upper()

    sp = tim_san_pham_theo_ma(ma_sp, danh_sach)
    if sp is None:
        print(f"  [!] Khong tim thay san pham co ma '{ma_sp}'.")
        return

    # In chi tiet san pham truoc khi xac nhan xoa
    print(f"\n  --- THONG TIN SAN PHAM SE XOA ---")
    print(f"  Ma SP        : {sp.ma_sp}")
    print(f"  Ten san pham : {sp.ten_sp}")
    print(f"  So luong ton : {sp.so_luong_ton} {sp.don_vi_tinh}")
    print(f"  ---------------------------------")

    if sp.so_luong_ton > 0:
        print(f"  [!] San pham '{sp.ten_sp}' con {sp.so_luong_ton} {sp.don_vi_tinh} trong kho.")
        print("  Khong the xoa san pham con hang. Hay xuat het hang truoc.")
        return

    # Cho phep an 'q' de huy
    xac_nhan = input(f"  Xac nhan xoa '{sp.ten_sp}' ({ma_sp})? (y/n, hoac 'q' de huy): ").strip().lower()
    if xac_nhan == 'q' or xac_nhan != 'y':
        print("  Da huy thao tac xoa.")
        return

    danh_sach_moi = []
    for item in danh_sach:
        if item.ma_sp != ma_sp:
            danh_sach_moi.append(item)

    if luu_danh_sach_san_pham(danh_sach_moi):
        print(f"  [OK] Da xoa san pham '{sp.ten_sp}' ({ma_sp}).")
    else:
        print("  [LOI] Khong the luu thay doi.")


def hien_thi_tat_ca_san_pham():
    """Hien thi toan bo danh muc san pham."""
    danh_sach = tai_danh_sach_san_pham()
    if not danh_sach:
        print("\n  Kho hang trong rong. Chua co san pham nao.")
        return

    print("\n" + "=" * 90)
    print(f"{'DANH MUC SAN PHAM KHO HANG':^90}")
    print("=" * 90)
    print(f"  {'Ma SP':<10} {'Ten san pham':<25} {'Loai hang':<18} {'DVT':<8} {'Ton kho':>8} {'Don gia':>14} {'Trang thai'}")
    print("-" * 90)

    for sp in danh_sach:
        trang_thai = "[!] SAP HET" if sp.sap_het_hang() else "On dinh"
        print(f"  {sp.ma_sp:<10} {sp.ten_sp:<25} {sp.loai_hang:<18} {sp.don_vi_tinh:<8} "
              f"{sp.so_luong_ton:>8} {sp.don_gia:>14,.0f} {trang_thai}")

    print("=" * 90)
    print(f"  Tong so san pham: {len(danh_sach)}")


# ============================================================
#  PHAN 3: NHAP KHO
# ============================================================

def nhap_kho():
    """Ghi nhan giao dich nhap kho."""
    print("\n--- NHAP KHO ---")
    danh_sach_sp = tai_danh_sach_san_pham()
    if not danh_sach_sp:
        print("  Chua co san pham nao. Vui long them san pham truoc.")
        return

    _in_bang_san_pham(danh_sach_sp, "DANH SACH SAN PHAM TRONG KHO")

    ma_sp = _nhap_chuoi_an_toan("  Nhap ma san pham can nhap kho")
    if ma_sp is None:
        return print("  Da huy thao tac nhap kho.")
    ma_sp = ma_sp.upper()


    sp = tim_san_pham_theo_ma(ma_sp, danh_sach_sp)
    if sp is None:
        print(f"  [!] Khong tim thay san pham co ma '{ma_sp}'.")
        return

    print(f"\n  Da chon: [{sp.ma_sp}] {sp.ten_sp} | Loai: {sp.loai_hang} "
          f"| Ton kho hien tai: {sp.so_luong_ton} {sp.don_vi_tinh}")

    so_luong = _nhap_so_nguyen_duong("  So luong nhap")
    if so_luong is None:  # Bắt None
        print("  Da huy thao tac nhap kho.")
        return
    don_gia  = _nhap_so_thuc_duong(
        f"  Don gia nhap [mac dinh {sp.don_gia:,.0f} VND, Enter de giu]",
        mac_dinh=sp.don_gia
    )
    if don_gia is None:  # Bắt None
        print("  Da huy thao tac nhap kho.")
        return
    ghi_chu = input("  Ghi chu (Enter bo qua, hoac 'q' de huy): ").strip()
    if ghi_chu.lower() == 'q': return print("  Da huy thao tac nhap kho.")
    ghi_chu = _lam_sach_chuoi(ghi_chu) # Lọc ký tự bẩn trong ghi chú
    ngay    = _lay_ngay_hom_nay()

    so_luong_cu = sp.so_luong_ton
    sp.so_luong_ton += so_luong
    luu_danh_sach_san_pham(danh_sach_sp)

    ma_gd = sinh_ma_giao_dich()
    giao_dich = GiaoDich(
        ma_gd=ma_gd, ma_sp=ma_sp, ten_sp=sp.ten_sp,
        loai_giao_dich=GiaoDich.LOAI_NHAP,
        so_luong=so_luong, don_gia=don_gia,
        ngay_thuc_hien=ngay, ghi_chu=ghi_chu
    )
    them_giao_dich(giao_dich)

    print(f"\n  [OK] NHAP KHO THANH CONG!")
    print(f"       Ma GD     : {ma_gd}")
    print(f"       San pham  : {sp.ten_sp} ({ma_sp})")
    print(f"       So luong  : +{so_luong} {sp.don_vi_tinh}")
    print(f"       Ton kho   : {so_luong_cu} -> {sp.so_luong_ton} {sp.don_vi_tinh}")
    print(f"       Thanh tien: {so_luong * don_gia:,.0f} VND | Ngay: {ngay}")


# ============================================================
#  PHAN 4: XUAT KHO
# ============================================================

def xuat_kho():
    """Ghi nhan giao dich xuat kho."""
    print("\n--- XUAT KHO ---")
    danh_sach_sp = tai_danh_sach_san_pham()
    if not danh_sach_sp:
        print("  Chua co san pham nao. Vui long them san pham truoc.")
        return

    _in_bang_san_pham(danh_sach_sp, "DANH SACH SAN PHAM TRONG KHO")

    # Su dung ham an toan de nhap ma SP
    ma_sp = _nhap_chuoi_an_toan("  Nhap ma san pham can xuat kho")
    if ma_sp is None:
        print("  Da huy thao tac xuat kho.")
        return
    ma_sp = ma_sp.upper()

    sp = tim_san_pham_theo_ma(ma_sp, danh_sach_sp)
    if sp is None:
        print(f"  [!] Khong tim thay san pham co ma '{ma_sp}'.")
        return

    print(f"\n  Da chon: [{sp.ma_sp}] {sp.ten_sp} | Loai: {sp.loai_hang} "
          f"| Ton kho hien tai: {sp.so_luong_ton} {sp.don_vi_tinh}")

    if sp.so_luong_ton == 0:
        print("  [!] San pham nay da het hang, khong the xuat them!")
        return

    so_luong = _nhap_so_nguyen_duong("  So luong xuat")
    if so_luong is None:
        print("  Da huy thao tac xuat kho.")
        return

    if so_luong > sp.so_luong_ton:
        print(f"  [!] Khong du hang! Ton kho chi con {sp.so_luong_ton} {sp.don_vi_tinh}, ban muon xuat {so_luong}.")
        return

    don_gia = _nhap_so_thuc_duong(
        f"  Don gia xuat [mac dinh {sp.don_gia:,.0f} VND, Enter de giu]",
        mac_dinh=sp.don_gia
    )
    if don_gia is None:
        print("  Da huy thao tac xuat kho.")
        return
        
    # Cho phep huy ca o buoc ghi chu, lam sach chuoi rac
    ghi_chu = input("  Ghi chu (Enter bo qua, hoac 'q' de huy): ").strip()
    if ghi_chu.lower() == 'q':
        print("  Da huy thao tac xuat kho.")
        return
    ghi_chu = _lam_sach_chuoi(ghi_chu)

    ngay = _lay_ngay_hom_nay()
    
    so_luong_cu = sp.so_luong_ton
    sp.so_luong_ton -= so_luong
    luu_danh_sach_san_pham(danh_sach_sp)

    ma_gd = sinh_ma_giao_dich()
    giao_dich = GiaoDich(
        ma_gd=ma_gd, ma_sp=ma_sp, ten_sp=sp.ten_sp,
        loai_giao_dich=GiaoDich.LOAI_XUAT,
        so_luong=so_luong, don_gia=don_gia,
        ngay_thuc_hien=ngay, ghi_chu=ghi_chu
    )
    them_giao_dich(giao_dich)

    print(f"\n  [OK] XUAT KHO THANH CONG!")
    print(f"       Ma GD     : {ma_gd}")
    print(f"       San pham  : {sp.ten_sp} ({ma_sp})")
    print(f"       So luong  : -{so_luong} {sp.don_vi_tinh}")
    print(f"       Ton kho   : {so_luong_cu} -> {sp.so_luong_ton} {sp.don_vi_tinh}")
    print(f"       Thanh tien: {so_luong * don_gia:,.0f} VND | Ngay: {ngay}")

    if sp.sap_het_hang():
        print()
        print("  " + "!" * 55)
        print(f"  [CANH BAO] '{sp.ten_sp}' sap het hang!")
        print(f"  Ton kho con lai: {sp.so_luong_ton} {sp.don_vi_tinh} "
              f"(nguong toi thieu: {sp.nguong_toi_thieu})")
        print("  " + "!" * 55)


# ============================================================
#  TIEN ICH NOI BO
# ============================================================

def _lam_sach_chuoi(chuoi):
    """Loai bo cac ky tu dac biet de tranh du lieu rac."""
    ky_tu_cam = ['"', "'", '*', '~', '`', '#', '$', '%', '^', '&', '\\', '|']
    ket_qua = chuoi
    for kt in ky_tu_cam:
        ket_qua = ket_qua.replace(kt, "")
    # Thay the nhieu khoang trang thanh 1 khoang trang
    return " ".join(ket_qua.split())

def _lay_ngay_hom_nay():
    return datetime.date.today().strftime("%Y-%m-%d")


def _nhap_so_nguyen_duong(nhan_hien_thi):
    while True:
        nhap = input(f"{nhan_hien_thi} (hoac nhap 'q' de huy): ").strip()
        if nhap.lower() == 'q':
            return None # Tra ve None neu nguoi dung muon huy
            
        try:
            gia_tri = int(nhap)
            if gia_tri <= 0:
                print("  [!] Gia tri phai la so nguyen duong (> 0).")
                continue
            return gia_tri
        except ValueError:
            print("  [!] Vui long nhap so nguyen hop le.")


def _nhap_so_thuc_duong(nhan_hien_thi, mac_dinh=None):
    while True:
        nhap = input(f"{nhan_hien_thi} (hoac nhap 'q' de huy): ").strip().replace(",", "")
        if nhap.lower() == 'q':
            return None # Tra ve None neu nguoi dung muon huy
            
        if nhap == "" and mac_dinh is not None:
            return mac_dinh
        try:
            gia_tri = float(nhap)
            if gia_tri <= 0:
                print("  [!] Gia tri phai lon hon 0.")
                continue
            return gia_tri
        except ValueError:
            print("  [!] Vui long nhap so hop le.")

def _nhap_chuoi_an_toan(nhan_hien_thi, cho_phep_rong=False):
    """Nhap chuoi, loc ky tu dac biet va cho phep nhap 'q' de huy."""
    while True:
        nhap = input(f"{nhan_hien_thi} (hoac 'q' de huy): ").strip()
        if nhap.lower() == 'q':
            return None # Nguoi dung muon huy
            
        nhap = _lam_sach_chuoi(nhap)
        
        if not nhap and not cho_phep_rong:
            print("  [!] Thong tin khong duoc de trong hoac chi chua ky tu dac biet.")
            continue
        return nhap
