# report.py - Bao cao nhat ky nhap/xuat kho va thong ke gia tri ton kho
# Tu cai dat xu ly, sap xep, thong ke - khong dung thu vien nang cao

from storage import tai_danh_sach_san_pham, tai_danh_sach_giao_dich
from models import GiaoDich
import datetime


# ============================================================
#  PHAN 1: NHAT KY NHAP/XUAT KHO THEO THANG
# ============================================================

def _thong_ke_ky_co_san(tat_ca_giao_dich):
    """
    Phan tich danh sach giao dich de tim cac nam/thang co du lieu.
    Tra ve dict: { nam (int): [thang1, thang2, ...] } da sap xep.
    Tu cai dat - khong dung sort() hay dict built-in advanced.
    """
    # Dung mang de luu cap (nam, thang) duy nhat
    cap_nam_thang = []
    for gd in tat_ca_giao_dich:
        phan = gd.ngay_thuc_hien.split("-")
        if len(phan) >= 2:
            nam  = int(phan[0])
            thang = int(phan[1])
            # Kiem tra da co chua (tu cai dat)
            da_co = False
            for cap in cap_nam_thang:
                if cap[0] == nam and cap[1] == thang:
                    da_co = True
                    break
            if not da_co:
                cap_nam_thang.append([nam, thang])

    # Sap xep tang dan theo nam roi thang (bubble sort tu cai dat)
    n = len(cap_nam_thang)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            a, b = cap_nam_thang[j], cap_nam_thang[j + 1]
            if a[0] > b[0] or (a[0] == b[0] and a[1] > b[1]):
                cap_nam_thang[j], cap_nam_thang[j + 1] = b, a

    # Nhom theo nam
    nhom_nam = []   # [[nam, [thang1, thang2, ...]], ...]
    for cap in cap_nam_thang:
        nam, thang = cap[0], cap[1]
        tim_thay = False
        for nhom in nhom_nam:
            if nhom[0] == nam:
                nhom[1].append(thang)
                tim_thay = True
                break
        if not tim_thay:
            nhom_nam.append([nam, [thang]])

    return nhom_nam


def bao_cao_theo_thang():
    """
    Hien thi nhat ky giao dich (nhap/xuat) trong mot thang cu the.
    In ra cac ky co du lieu truoc khi hoi nguoi dung nhap thang/nam.
    """
    print("\n--- BAO CAO NHAT KY NHAP/XUAT KHO THEO THANG ---")

    tat_ca_giao_dich = tai_danh_sach_giao_dich()

    # In thong tin cac ky co du lieu
    nhom_nam = _thong_ke_ky_co_san(tat_ca_giao_dich)
    print()
    if not nhom_nam:
        print("  (Chua co giao dich nao duoc ghi nhan)")
    else:
        print("  Du lieu hien co trong he thong:")
        print("  " + "-" * 45)
        for nhom in nhom_nam:
            nam = nhom[0]
            ds_thang = nhom[1]
            thang_str = ", ".join([f"Thang {t}" for t in ds_thang])
            dem_gd_nam = 0
            for gd in tat_ca_giao_dich:
                if gd.ngay_thuc_hien.startswith(str(nam)):
                    dem_gd_nam += 1
            print(f"  Nam {nam} ({dem_gd_nam} giao dich): {thang_str}")
        print("  " + "-" * 45)
        # Goi y ky som nhat va moi nhat
        ky_dau = nhom_nam[0]
        ky_cuoi = nhom_nam[-1]
        print(f"  => Du lieu tu Thang {ky_dau[1][0]}/{ky_dau[0]} "
              f"den Thang {ky_cuoi[1][-1]}/{ky_cuoi[0]}")
    print()

    # Nhap nam
    while True:
        nhap_nam = input("  Nhap nam (VD: 2025) hoac 'q' de huy: ").strip()
        if nhap_nam.lower() == 'q': return # Thoát ngay lập tức
        try:
            nam = int(nhap_nam)
            if 2000 <= nam <= 2100: break
            print("  [!] Nam khong hop le.")
        except ValueError:
            print("  [!] Vui long nhap so nguyen.")

    # Nhap thang
    while True:
        nhap_thang = input("  Nhap thang (1-12) hoac 'q' de huy: ").strip()
        if nhap_thang.lower() == 'q': return
        try:
            thang = int(nhap_thang)
            if 1 <= thang <= 12: break
            print("  [!] Thang phai tu 1 den 12.")
        except ValueError:
            print("  [!] Vui long nhap so nguyen.")

    prefix_thang = f"{nam}-{thang:02d}"

    # Loc giao dich trong thang
    tat_ca_giao_dich = tai_danh_sach_giao_dich()
    giao_dich_trong_thang = _loc_giao_dich_theo_thang(tat_ca_giao_dich, prefix_thang)

    # Phan loai nhap / xuat
    ds_nhap = []
    ds_xuat = []
    for gd in giao_dich_trong_thang:
        if gd.loai_giao_dich == GiaoDich.LOAI_NHAP:
            ds_nhap.append(gd)
        else:
            ds_xuat.append(gd)

    print("\n" + "=" * 95)
    print(f"{'NHAT KY KHO HANG THANG ' + str(thang) + '/' + str(nam):^95}")
    print("=" * 95)

    # --- Nhap kho ---
    print(f"\n  [NHAP KHO] - {len(ds_nhap)} phieu")
    if ds_nhap:
        _in_bang_giao_dich(ds_nhap)
        tong_nhap = _tinh_tong_thanh_tien(ds_nhap)
        print(f"  => Tong tien nhap: {tong_nhap:,.0f} VND")
    else:
        print("  Khong co giao dich nhap kho nao trong thang nay.")

    # --- Xuat kho ---
    print(f"\n  [XUAT KHO] - {len(ds_xuat)} phieu")
    if ds_xuat:
        _in_bang_giao_dich(ds_xuat)
        tong_xuat = _tinh_tong_thanh_tien(ds_xuat)
        print(f"  => Tong tien xuat: {tong_xuat:,.0f} VND")
    else:
        print("  Khong co giao dich xuat kho nao trong thang nay.")

    print("\n" + "=" * 95)
    if giao_dich_trong_thang:
        tong = _tinh_tong_thanh_tien(giao_dich_trong_thang)
        print(f"  Tong so giao dich : {len(giao_dich_trong_thang)}")
        print(f"  Tong gia tri GD   : {tong:,.0f} VND")
    else:
        print(f"  Khong co giao dich nao trong thang {thang}/{nam}.")
    print("=" * 95)


def _loc_giao_dich_theo_thang(danh_sach, prefix_thang):
    """
    Loc thu cong cac giao dich trong thang.
    prefix_thang dang 'YYYY-MM'.
    """
    ket_qua = []
    for gd in danh_sach:
        if gd.ngay_thuc_hien.startswith(prefix_thang):
            ket_qua.append(gd)
    return ket_qua


def _in_bang_giao_dich(danh_sach):
    """In bang danh sach giao dich dang bang."""
    print(f"  {'Ma GD':<8} {'Ngay':<12} {'Ma SP':<8} {'Ten san pham':<22} "
          f"{'SL':>6} {'Don gia':>12} {'Thanh tien':>14}")
    print("  " + "-" * 88)
    for gd in danh_sach:
        print(f"  {gd.ma_gd:<8} {gd.ngay_thuc_hien:<12} {gd.ma_sp:<8} {gd.ten_sp:<22} "
              f"{gd.so_luong:>6} {gd.don_gia:>12,.0f} {gd.thanh_tien():>14,.0f}")


def _tinh_tong_thanh_tien(danh_sach):
    """Tinh tong thanh tien tu mang giao dich (tu cai dat)."""
    tong = 0
    for gd in danh_sach:
        tong += gd.thanh_tien()
    return tong


# ============================================================
#  PHAN 2: THONG KE GIA TRI HANG TON KHO HIEN TAI
# ============================================================

def thong_ke_gia_tri_ton_kho():
    """
    Hien thi bao cao gia tri ton kho hien tai:
    - Gia tri tung san pham = so_luong_ton * don_gia
    - Tong gia tri toan kho
    - Thong ke theo tung loai hang
    """
    print("\n--- THONG KE GIA TRI HANG TON KHO HIEN TAI ---")
    danh_sach = tai_danh_sach_san_pham()

    if not danh_sach:
        print("  Kho hang trong rong.")
        return

    # Sap xep giam dan theo gia tri ton kho (bubble sort tu cai dat)
    ds_sap_xep = _sap_xep_giam_dan_gia_tri(danh_sach)

    print("\n" + "=" * 90)
    print(f"{'THONG KE GIA TRI TON KHO':^90}")
    print(f"{'Ngay lap: ' + datetime.date.today().strftime('%d/%m/%Y'):^90}")
    print("=" * 90)
    print(f"  {'STT':<5} {'Ma SP':<10} {'Ten san pham':<25} {'DVT':<8} "
          f"{'Ton kho':>8} {'Don gia':>14} {'Gia tri ton':>14}")
    print("  " + "-" * 88)

    tong_gia_tri = 0
    stt = 1
    for sp in ds_sap_xep:
        gia_tri = sp.thanh_tien()
        tong_gia_tri += gia_tri
        print(f"  {stt:<5} {sp.ma_sp:<10} {sp.ten_sp:<25} {sp.don_vi_tinh:<8} "
              f"{sp.so_luong_ton:>8} {sp.don_gia:>14,.0f} {gia_tri:>14,.0f}")
        stt += 1

    print("  " + "=" * 88)
    print(f"  {'TONG GIA TRI TON KHO':>76} {tong_gia_tri:>14,.0f}")
    print("  " + "=" * 88)

    # Thong ke theo loai hang
    print("\n  --- PHAN TICH THEO LOAI HANG ---")
    _thong_ke_theo_loai(danh_sach)


def _sap_xep_giam_dan_gia_tri(danh_sach):
    """
    Sap xep giam dan theo gia tri ton kho bang bubble sort tu cai dat.
    Tra ve mang moi (ban sao).
    """
    ket_qua = []
    for sp in danh_sach:
        ket_qua.append(sp)

    n = len(ket_qua)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if ket_qua[j].thanh_tien() < ket_qua[j + 1].thanh_tien():
                ket_qua[j], ket_qua[j + 1] = ket_qua[j + 1], ket_qua[j]
    return ket_qua


def _thong_ke_theo_loai(danh_sach):
    """
    Nhom san pham theo loai hang va tinh tong gia tri tung nhom.
    Tu cai dat: dung mang de luu cap (loai, tong_gia_tri, so_sp).
    """
    # Mang luu: [ten_loai, tong_gia_tri, so_luong_sp]
    nhom = []

    for sp in danh_sach:
        tim_thay = False
        for i in range(len(nhom)):
            if nhom[i][0].lower() == sp.loai_hang.lower():
                nhom[i][1] += sp.thanh_tien()
                nhom[i][2] += 1
                tim_thay = True
                break
        if not tim_thay:
            nhom.append([sp.loai_hang, sp.thanh_tien(), 1])

    # Sap xep giam dan theo gia tri (bubble sort)
    n = len(nhom)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if nhom[j][1] < nhom[j + 1][1]:
                nhom[j], nhom[j + 1] = nhom[j + 1], nhom[j]

    tong_chung = 0
    for item in nhom:
        tong_chung += item[1]

    print(f"\n  {'Loai hang':<25} {'So SP':>6} {'Gia tri ton':>16} {'% Gia tri':>10}")
    print("  " + "-" * 62)
    for item in nhom:
        ten_loai, gia_tri, so_sp = item[0], item[1], item[2]
        phan_tram = (gia_tri / tong_chung * 100) if tong_chung > 0 else 0
        print(f"  {ten_loai:<25} {so_sp:>6} {gia_tri:>16,.0f} {phan_tram:>9.1f}%")
    print("  " + "=" * 62)
    print(f"  {'TONG CONG':<25} {len(danh_sach):>6} {tong_chung:>16,.0f} {'100.0%':>10}")
    return nhom


# ============================================================
#  PHAN 3: BAO CAO NHANH (cho menu kiem ke)
# ============================================================

def kiem_ke_tong_hop():
    """
    Bao cao kiem ke tong hop nhanh: hien thi toan bo san pham va
    ket hop voi canh bao san pham sap het hang.
    """
    danh_sach = tai_danh_sach_san_pham()
    giao_dich = tai_danh_sach_giao_dich()

    print("\n" + "=" * 80)
    print(f"{'KIEM KE KHO HANG TONG HOP':^80}")
    print(f"{'Ngay: ' + datetime.date.today().strftime('%d/%m/%Y'):^80}")
    print("=" * 80)

    tong_sp = len(danh_sach)
    tong_gia_tri = 0
    dem_sap_het = 0
    dem_het_hang = 0

    for sp in danh_sach:
        tong_gia_tri += sp.thanh_tien()
        if sp.so_luong_ton == 0:
            dem_het_hang += 1
        elif sp.sap_het_hang():
            dem_sap_het += 1

    tong_gd = len(giao_dich)
    dem_nhap = 0
    dem_xuat = 0
    for gd in giao_dich:
        if gd.loai_giao_dich == GiaoDich.LOAI_NHAP:
            dem_nhap += 1
        else:
            dem_xuat += 1

    print(f"\n  TONG QUAN:")
    print(f"    Tong so san pham         : {tong_sp}")
    print(f"    Gia tri ton kho hien tai : {tong_gia_tri:,.0f} VND")
    print(f"    San pham sap het hang    : {dem_sap_het}")
    print(f"    San pham het hang        : {dem_het_hang}")
    print(f"\n  GIAO DICH:")
    print(f"    Tong giao dich da ghi    : {tong_gd}")
    print(f"    - Nhap kho               : {dem_nhap}")
    print(f"    - Xuat kho               : {dem_xuat}")
    print("=" * 80)
