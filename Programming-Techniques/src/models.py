# models.py - Cau truc du lieu cua he thong quan ly kho hang
# Khong su dung cac thu vien cau truc du lieu co san

class SanPham:
    """Lop dai dien cho mot san pham trong kho"""

    def __init__(self, ma_sp, ten_sp, loai_hang, don_vi_tinh,
                 so_luong_ton, don_gia, nguong_toi_thieu):
        self.ma_sp = ma_sp                      # Ma san pham (chuoi, duy nhat)
        self.ten_sp = ten_sp                    # Ten san pham
        self.loai_hang = loai_hang              # Loai hang (VD: Thuc pham, Dien tu, ...)
        self.don_vi_tinh = don_vi_tinh          # Don vi tinh (cai, kg, thung, ...)
        self.so_luong_ton = so_luong_ton        # So luong ton kho hien tai
        self.don_gia = don_gia                  # Don gia (VND)
        self.nguong_toi_thieu = nguong_toi_thieu  # Nguong canh bao ton kho

    def thanh_tien(self):
        """Tinh gia tri ton kho cua san pham"""
        return self.so_luong_ton * self.don_gia

    def sap_het_hang(self):
        """Kiem tra xem san pham co sap het hang khong"""
        return self.so_luong_ton <= self.nguong_toi_thieu

    def to_dict(self):
        """Chuyen doi doi tuong thanh dictionary de luu file JSON"""
        return {
            "ma_sp": self.ma_sp,
            "ten_sp": self.ten_sp,
            "loai_hang": self.loai_hang,
            "don_vi_tinh": self.don_vi_tinh,
            "so_luong_ton": self.so_luong_ton,
            "don_gia": self.don_gia,
            "nguong_toi_thieu": self.nguong_toi_thieu
        }

    @staticmethod
    def from_dict(d):
        """Tao doi tuong SanPham tu dictionary (doc tu file JSON)"""
        return SanPham(
            ma_sp=d["ma_sp"],
            ten_sp=d["ten_sp"],
            loai_hang=d["loai_hang"],
            don_vi_tinh=d["don_vi_tinh"],
            so_luong_ton=d["so_luong_ton"],
            don_gia=d["don_gia"],
            nguong_toi_thieu=d["nguong_toi_thieu"]
        )

    def __str__(self):
        trang_thai = " [!] SAP HET HANG" if self.sap_het_hang() else ""
        return (f"[{self.ma_sp}] {self.ten_sp} | Loai: {self.loai_hang} | "
                f"DVT: {self.don_vi_tinh} | Ton: {self.so_luong_ton} | "
                f"Don gia: {self.don_gia:,.0f} VND{trang_thai}")


class GiaoDich:
    """Lop dai dien cho mot giao dich nhap/xuat kho"""

    LOAI_NHAP = "nhap"
    LOAI_XUAT = "xuat"

    def __init__(self, ma_gd, ma_sp, ten_sp, loai_giao_dich,
                 so_luong, don_gia, ngay_thuc_hien, ghi_chu=""):
        self.ma_gd = ma_gd                          # Ma giao dich (tu sinh)
        self.ma_sp = ma_sp                          # Ma san pham lien quan
        self.ten_sp = ten_sp                        # Ten san pham (luu de bao cao)
        self.loai_giao_dich = loai_giao_dich        # "nhap" hoac "xuat"
        self.so_luong = so_luong                    # So luong giao dich
        self.don_gia = don_gia                      # Don gia tai thoi diem giao dich
        self.ngay_thuc_hien = ngay_thuc_hien        # Ngay thuc hien (chuoi YYYY-MM-DD)
        self.ghi_chu = ghi_chu                      # Ghi chu them (tuy chon)

    def thanh_tien(self):
        """Tinh tong tien giao dich"""
        return self.so_luong * self.don_gia

    def to_dict(self):
        """Chuyen doi doi tuong thanh dictionary de luu file JSON"""
        return {
            "ma_gd": self.ma_gd,
            "ma_sp": self.ma_sp,
            "ten_sp": self.ten_sp,
            "loai_giao_dich": self.loai_giao_dich,
            "so_luong": self.so_luong,
            "don_gia": self.don_gia,
            "ngay_thuc_hien": self.ngay_thuc_hien,
            "ghi_chu": self.ghi_chu
        }

    @staticmethod
    def from_dict(d):
        """Tao doi tuong GiaoDich tu dictionary (doc tu file JSON)"""
        return GiaoDich(
            ma_gd=d["ma_gd"],
            ma_sp=d["ma_sp"],
            ten_sp=d.get("ten_sp", ""),
            loai_giao_dich=d["loai_giao_dich"],
            so_luong=d["so_luong"],
            don_gia=d["don_gia"],
            ngay_thuc_hien=d["ngay_thuc_hien"],
            ghi_chu=d.get("ghi_chu", "")
        )

    def __str__(self):
        loai_str = "NHAP KHO" if self.loai_giao_dich == self.LOAI_NHAP else "XUAT KHO"
        return (f"[{self.ma_gd}] {self.ngay_thuc_hien} | {loai_str} | "
                f"SP: {self.ten_sp} ({self.ma_sp}) | "
                f"SL: {self.so_luong} | Don gia: {self.don_gia:,.0f} VND | "
                f"Thanh tien: {self.thanh_tien():,.0f} VND")
