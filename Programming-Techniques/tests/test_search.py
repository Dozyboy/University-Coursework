import unittest
import search
from models import SanPham

class TestSearch(unittest.TestCase):
    def setUp(self):
        # Thiết lập danh sách sản phẩm mẫu để tìm kiếm và sắp xếp
        self.sp1 = SanPham("SP001", "Sữa tươi Vinamilk", "Thực phẩm", "hộp", 100, 15000, 20)
        self.sp2 = SanPham("SP002", "Bánh quy Cosy", "Thực phẩm", "gói", 15, 25000, 20) # Sắp hết hàng (15 <= 20)
        self.sp3 = SanPham("SP003", "Bàn chải Colgate", "Tiêu dùng", "cái", 5, 12000, 10) # Sắp hết hàng (5 <= 10)
        self.sp4 = SanPham("SP004", "Bia Heineken", "Đồ uống", "lon", 50, 22000, 5)
        
        self.danh_sach = [self.sp1, self.sp2, self.sp3, self.sp4]

    def test_chuan_hoa(self):
        self.assertEqual(search._chuan_hoa("  SP001  "), "sp001")
        self.assertEqual(search._chuan_hoa("Thực Phẩm"), "thực phẩm")

    def test_tim_kiem_theo_ma(self):
        # Khớp chính xác tuyệt đối không phân biệt hoa thường
        res = search.tim_kiem_theo_ma("sp001", self.danh_sach)
        self.assertEqual(res, self.sp1)

        res2 = search.tim_kiem_theo_ma("  SP002  ", self.danh_sach)
        self.assertEqual(res2, self.sp2)

        res_none = search.tim_kiem_theo_ma("SP999", self.danh_sach)
        self.assertIsNone(res_none)

    def test_tim_kiem_theo_ten(self):
        # Khớp một phần
        res = search.tim_kiem_theo_ten("sữa", self.danh_sach)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], self.sp1)

        # Khớp nhiều sản phẩm
        res2 = search.tim_kiem_theo_ten("b", self.danh_sach) # Bánh, Bàn chải, Bia
        self.assertEqual(len(res2), 3)

        # Không khớp
        res_none = search.tim_kiem_theo_ten("không tồn tại", self.danh_sach)
        self.assertEqual(len(res_none), 0)

    def test_tim_kiem_theo_loai(self):
        res = search.tim_kiem_theo_loai("thực phẩm", self.danh_sach)
        self.assertEqual(len(res), 2)
        self.assertIn(self.sp1, res)
        self.assertIn(self.sp2, res)

        res2 = search.tim_kiem_theo_loai("đồ uống", self.danh_sach)
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0], self.sp4)

    def test_loc_san_pham_sap_het_hang(self):
        # sp2 (tồn 15, ngưỡng 20), sp3 (tồn 5, ngưỡng 10)
        # Sắp xếp tăng dần theo lượng tồn kho -> sp3 trước sp2
        res = search.loc_san_pham_sap_het_hang(self.danh_sach)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], self.sp3) # Tồn 5
        self.assertEqual(res[1], self.sp2) # Tồn 15

    def test_sap_xep_theo_ten(self):
        # Sắp xếp A-Z theo mã Unicode của ký tự:
        # 1. "Bia Heineken" (b-i, 'i' = 105)
        # 2. "Bàn chải Colgate" (b-à, 'à' = 224)
        # 3. "Bánh quy Cosy" (b-á, 'á' = 225)
        # 4. "Sữa tươi Vinamilk" (s-ũ, 's' = 115)
        res = search.sap_xep_theo_ten(self.danh_sach)
        self.assertEqual(len(res), 4)
        self.assertEqual(res[0].ten_sp, "Bia Heineken")
        self.assertEqual(res[1].ten_sp, "Bàn chải Colgate")
        self.assertEqual(res[2].ten_sp, "Bánh quy Cosy")
        self.assertEqual(res[3].ten_sp, "Sữa tươi Vinamilk")

if __name__ == "__main__":
    unittest.main()
