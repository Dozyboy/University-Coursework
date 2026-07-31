import unittest
from models import SanPham, GiaoDich

class TestSanPhamModel(unittest.TestCase):
    def setUp(self):
        self.sp = SanPham(
            ma_sp="SP001",
            ten_sp="Sữa tươi Vinamilk",
            loai_hang="Thực phẩm",
            don_vi_tinh="hộp",
            so_luong_ton=100,
            don_gia=15000,
            nguong_toi_thieu=20
        )

    def test_initialization(self):
        self.assertEqual(self.sp.ma_sp, "SP001")
        self.assertEqual(self.sp.ten_sp, "Sữa tươi Vinamilk")
        self.assertEqual(self.sp.loai_hang, "Thực phẩm")
        self.assertEqual(self.sp.don_vi_tinh, "hộp")
        self.assertEqual(self.sp.so_luong_ton, 100)
        self.assertEqual(self.sp.don_gia, 15000)
        self.assertEqual(self.sp.nguong_toi_thieu, 20)

    def test_thanh_tien(self):
        # 100 * 15000 = 1,500,000
        self.assertEqual(self.sp.thanh_tien(), 1500000)

    def test_sap_het_hang(self):
        # 100 > 20 -> False
        self.assertFalse(self.sp.sap_het_hang())
        
        # 20 <= 20 -> True
        self.sp.so_luong_ton = 20
        self.assertTrue(self.sp.sap_het_hang())
        
        # 5 < 20 -> True
        self.sp.so_luong_ton = 5
        self.assertTrue(self.sp.sap_het_hang())

    def test_to_dict_and_from_dict(self):
        d = self.sp.to_dict()
        self.assertEqual(d["ma_sp"], "SP001")
        self.assertEqual(d["so_luong_ton"], 100)
        
        sp2 = SanPham.from_dict(d)
        self.assertEqual(sp2.ma_sp, self.sp.ma_sp)
        self.assertEqual(sp2.ten_sp, self.sp.ten_sp)
        self.assertEqual(sp2.thanh_tien(), self.sp.thanh_tien())

    def test_str_representation(self):
        s = str(self.sp)
        self.assertIn("SP001", s)
        self.assertIn("Sữa tươi Vinamilk", s)


class TestGiaoDichModel(unittest.TestCase):
    def setUp(self):
        self.gd = GiaoDich(
            ma_gd="GD0001",
            ma_sp="SP001",
            ten_sp="Sữa tươi Vinamilk",
            loai_giao_dich="nhap",
            so_luong=50,
            don_gia=14000,
            ngay_thuc_hien="2025-05-15",
            ghi_chu="Nhập hàng tháng 5"
        )

    def test_initialization(self):
        self.assertEqual(self.gd.ma_gd, "GD0001")
        self.assertEqual(self.gd.ma_sp, "SP001")
        self.assertEqual(self.gd.ten_sp, "Sữa tươi Vinamilk")
        self.assertEqual(self.gd.loai_giao_dich, "nhap")
        self.assertEqual(self.gd.so_luong, 50)
        self.assertEqual(self.gd.don_gia, 14000)
        self.assertEqual(self.gd.ngay_thuc_hien, "2025-05-15")
        self.assertEqual(self.gd.ghi_chu, "Nhập hàng tháng 5")

    def test_thanh_tien(self):
        # 50 * 14000 = 700,000
        self.assertEqual(self.gd.thanh_tien(), 700000)

    def test_to_dict_and_from_dict(self):
        d = self.gd.to_dict()
        self.assertEqual(d["ma_gd"], "GD0001")
        self.assertEqual(d["so_luong"], 50)
        
        gd2 = GiaoDich.from_dict(d)
        self.assertEqual(gd2.ma_gd, self.gd.ma_gd)
        self.assertEqual(gd2.ma_sp, self.gd.ma_sp)
        self.assertEqual(gd2.thanh_tien(), self.gd.thanh_tien())

    def test_str_representation(self):
        s = str(self.gd)
        self.assertIn("GD0001", s)
        self.assertIn("NHAP KHO", s)
        self.assertIn("Sữa tươi Vinamilk", s)
        
        # Test for xuat kho
        self.gd.loai_giao_dich = "xuat"
        s2 = str(self.gd)
        self.assertIn("XUAT KHO", s2)

if __name__ == "__main__":
    unittest.main()
