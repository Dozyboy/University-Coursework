import unittest
import os
import tempfile
import storage
from models import SanPham, GiaoDich

class TestStorage(unittest.TestCase):
    def setUp(self):
        # Thiết lập thư mục tạm và đổi các biến đường dẫn file trong storage
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_file_sp = storage.FILE_SAN_PHAM
        self.old_file_gd = storage.FILE_GIAO_DICH
        
        storage.FILE_SAN_PHAM = os.path.join(self.temp_dir.name, "products.json")
        storage.FILE_GIAO_DICH = os.path.join(self.temp_dir.name, "transactions.json")
        
        # Mẫu dữ liệu sản phẩm
        self.sp1 = SanPham("SP001", "Sản phẩm A", "Loại 1", "cái", 10, 1000, 5)
        self.sp2 = SanPham("SP002", "Sản phẩm B", "Loại 2", "hộp", 20, 2000, 2)
        
        # Mẫu giao dịch
        self.gd1 = GiaoDich("GD0001", "SP001", "Sản phẩm A", "nhap", 5, 1000, "2025-06-01")
        self.gd2 = GiaoDich("GD0002", "SP002", "Sản phẩm B", "xuat", 2, 2000, "2025-06-02")

    def tearDown(self):
        # Khôi phục các biến đường dẫn file gốc và dọn dẹp thư mục tạm
        storage.FILE_SAN_PHAM = self.old_file_sp
        storage.FILE_GIAO_DICH = self.old_file_gd
        self.temp_dir.cleanup()

    def test_products_save_and_load(self):
        # Khi chưa có file
        danh_sach = storage.tai_danh_sach_san_pham()
        self.assertEqual(len(danh_sach), 0)

        # Lưu danh sách
        ds_luu = [self.sp1, self.sp2]
        success = storage.luu_danh_sach_san_pham(ds_luu)
        self.assertTrue(success)

        # Tải lại danh sách
        ds_tai = storage.tai_danh_sach_san_pham()
        self.assertEqual(len(ds_tai), 2)
        self.assertEqual(ds_tai[0].ma_sp, "SP001")
        self.assertEqual(ds_tai[1].ten_sp, "Sản phẩm B")

    def test_transactions_save_and_load(self):
        # Khi chưa có file
        danh_sach = storage.tai_danh_sach_giao_dich()
        self.assertEqual(len(danh_sach), 0)

        # Lưu danh sách
        ds_luu = [self.gd1, self.gd2]
        success = storage.luu_danh_sach_giao_dich(ds_luu)
        self.assertTrue(success)

        # Tải lại danh sách
        ds_tai = storage.tai_danh_sach_giao_dich()
        self.assertEqual(len(ds_tai), 2)
        self.assertEqual(ds_tai[0].ma_gd, "GD0001")
        self.assertEqual(ds_tai[1].loai_giao_dich, "xuat")

    def test_them_giao_dich(self):
        # Thêm giao dịch mới
        success = storage.them_giao_dich(self.gd1)
        self.assertTrue(success)
        
        # Tải lại kiểm tra
        ds_tai = storage.tai_danh_sach_giao_dich()
        self.assertEqual(len(ds_tai), 1)
        self.assertEqual(ds_tai[0].ma_gd, "GD0001")

    def test_sinh_ma_giao_dich(self):
        # Chưa có GD nào -> trả về GD0001
        self.assertEqual(storage.sinh_ma_giao_dich(), "GD0001")

        # Đã có GD -> trả về mã tiếp theo
        storage.them_giao_dich(self.gd1)
        self.assertEqual(storage.sinh_ma_giao_dich(), "GD0002")

        # Có mã không liên tục hoặc lớn hơn
        gd_lon = GiaoDich("GD0099", "SP001", "A", "nhap", 1, 100, "2025-06-01")
        storage.them_giao_dich(gd_lon)
        self.assertEqual(storage.sinh_ma_giao_dich(), "GD0100")

    def test_kiem_tra_ma_sp_ton_tai(self):
        ds = [self.sp1, self.sp2]
        self.assertTrue(storage.kiem_tra_ma_sp_ton_tai("SP001", ds))
        self.assertFalse(storage.kiem_tra_ma_sp_ton_tai("SP999", ds))

    def test_tim_san_pham_theo_ma(self):
        ds = [self.sp1, self.sp2]
        sp = storage.tim_san_pham_theo_ma("SP002", ds)
        self.assertIsNotNone(sp)
        self.assertEqual(sp.ten_sp, "Sản phẩm B")
        
        sp_none = storage.tim_san_pham_theo_ma("SP999", ds)
        self.assertIsNone(sp_none)

if __name__ == "__main__":
    unittest.main()
