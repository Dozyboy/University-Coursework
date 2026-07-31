import unittest
import os
import tempfile
import categories

class TestCategories(unittest.TestCase):
    def setUp(self):
        # Tạo file tạm và đổi đường dẫn trong module categories
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_file_cat = categories.FILE_CATEGORIES
        categories.FILE_CATEGORIES = os.path.join(self.temp_dir.name, "categories.json")

    def tearDown(self):
        # Khôi phục đường dẫn và dọn dẹp thư mục tạm
        categories.FILE_CATEGORIES = self.old_file_cat
        self.temp_dir.cleanup()

    def test_tai_categories_default(self):
        # Khi chưa có file, sẽ tự tạo file với dữ liệu mặc định
        self.assertFalse(os.path.exists(categories.FILE_CATEGORIES))
        du_lieu = categories.tai_categories()
        
        self.assertTrue(os.path.exists(categories.FILE_CATEGORIES))
        self.assertIn("loai_hang", du_lieu)
        self.assertIn("don_vi_tinh", du_lieu)
        self.assertEqual(du_lieu["loai_hang"], categories.DEFAULT_LOAI_HANG)
        self.assertEqual(du_lieu["don_vi_tinh"], categories.DEFAULT_DON_VI_TINH)

    def test_them_loai_hang_moi(self):
        # Khởi tạo mặc định
        categories.tai_categories()
        
        # Thêm loại hàng mới chưa tồn tại
        success = categories.them_loai_hang_moi("Đồ chơi gia đình")
        self.assertTrue(success)
        
        # Kiểm tra xem đã có trong danh sách chưa
        du_lieu = categories.tai_categories()
        self.assertIn("Đồ chơi gia đình", du_lieu["loai_hang"])
        
        # Thêm loại hàng đã tồn tại (không phân biệt hoa thường)
        success_trung = categories.them_loai_hang_moi("đồ chơi gia đình")
        self.assertFalse(success_trung)

    def test_them_don_vi_tinh_moi(self):
        categories.tai_categories()
        
        # Thêm đơn vị tính mới
        success = categories.them_don_vi_tinh_moi("bộ")
        self.assertTrue(success)
        
        du_lieu = categories.tai_categories()
        self.assertIn("bộ", du_lieu["don_vi_tinh"])
        
        # Thêm trùng
        success_trung = categories.them_don_vi_tinh_moi("BỘ")
        self.assertFalse(success_trung)

if __name__ == "__main__":
    unittest.main()
