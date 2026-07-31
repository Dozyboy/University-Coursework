import unittest
import io
import sys
import report
from models import SanPham, GiaoDich

class TestReport(unittest.TestCase):
    def setUp(self):
        # Redirect stdout to prevent UnicodeEncodeError on Windows and keep output clean
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Mẫu giao dịch
        self.gd1 = GiaoDich("GD0001", "SP001", "Sản phẩm A", "nhap", 5, 1000, "2025-06-01")
        self.gd2 = GiaoDich("GD0002", "SP002", "Sản phẩm B", "xuat", 2, 2000, "2025-06-02")
        self.gd3 = GiaoDich("GD0003", "SP001", "Sản phẩm A", "nhap", 10, 1000, "2025-07-10")
        self.gd4 = GiaoDich("GD0004", "SP003", "Sản phẩm C", "nhap", 1, 5000, "2024-12-25")
        
        self.danh_sach_gd = [self.gd1, self.gd2, self.gd3, self.gd4]

        # Mẫu sản phẩm
        self.sp1 = SanPham("SP001", "Sản phẩm A", "Loại 1", "cái", 10, 1000, 5) # giá trị = 10,000
        self.sp2 = SanPham("SP002", "Sản phẩm B", "Loại 2", "hộp", 20, 2000, 2) # giá trị = 40,000
        self.sp3 = SanPham("SP003", "Sản phẩm C", "Loại 1", "cái", 2, 5000, 1)  # giá trị = 10,000

        self.danh_sach_sp = [self.sp1, self.sp2, self.sp3]

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    def test_thong_ke_ky_co_san(self):
        # Lọc và nhóm các kỳ năm/tháng
        # Kỳ có sẵn nên được sắp xếp tăng dần: [2024, [12]], [2025, [6, 7]]
        res = report._thong_ke_ky_co_san(self.danh_sach_gd)
        self.assertEqual(len(res), 2)
        
        # Năm 2024
        self.assertEqual(res[0][0], 2024)
        self.assertEqual(res[0][1], [12])
        
        # Năm 2025
        self.assertEqual(res[1][0], 2025)
        self.assertEqual(res[1][1], [6, 7])

    def test_loc_giao_dich_theo_thang(self):
        # Lọc giao dịch tháng 6/2025
        res = report._loc_giao_dich_theo_thang(self.danh_sach_gd, "2025-06")
        self.assertEqual(len(res), 2)
        self.assertIn(self.gd1, res)
        self.assertIn(self.gd2, res)

        # Lọc giao dịch tháng 12/2024
        res2 = report._loc_giao_dich_theo_thang(self.danh_sach_gd, "2024-12")
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0], self.gd4)

        # Không có giao dịch
        res_none = report._loc_giao_dich_theo_thang(self.danh_sach_gd, "2025-01")
        self.assertEqual(len(res_none), 0)

    def test_tinh_tong_thanh_tien(self):
        # gd1: 5 * 1000 = 5,000
        # gd2: 2 * 2000 = 4,000
        # gd3: 10 * 1000 = 10,000
        # gd4: 1 * 5000 = 5,000
        # Tổng = 24,000
        self.assertEqual(report._tinh_tong_thanh_tien(self.danh_sach_gd), 24000)

    def test_sap_xep_giam_dan_gia_tri(self):
        # sp2 (40k) > sp1 (10k) = sp3 (10k)
        # Sắp xếp giảm dần -> sp2 đứng đầu
        res = report._sap_xep_giam_dan_gia_tri(self.danh_sach_sp)
        self.assertEqual(res[0], self.sp2)
        self.assertEqual(res[0].thanh_tien(), 40000)

    def test_thong_ke_theo_loai(self):
        # Loại 1: sp1 (10k) + sp3 (10k) = 20k
        # Loại 2: sp2 (40k)
        # Sắp xếp giảm dần theo giá trị -> Loại 2 trước, Loại 1 sau
        res = report._thong_ke_theo_loai(self.danh_sach_sp)
        self.assertEqual(len(res), 2)
        
        # Nhóm thứ nhất: Loại 2
        self.assertEqual(res[0][0], "Loại 2")
        self.assertEqual(res[0][1], 40000) # giá trị
        self.assertEqual(res[0][2], 1)     # số SP
        
        # Nhóm thứ hai: Loại 1
        self.assertEqual(res[1][0], "Loại 1")
        self.assertEqual(res[1][1], 20000) # giá trị
        self.assertEqual(res[1][2], 2)     # số SP

if __name__ == "__main__":
    unittest.main()
