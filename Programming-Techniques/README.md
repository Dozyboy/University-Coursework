# Hệ thống Quản lý Kho hàng (Warehouse Management System)
### Nhóm G22 — Chủ đề 3 | Môn học: Kỹ thuật Lập trình

| Thành phần | Thông tin chi tiết |
|---|---|
| **Thành viên** | Thiệu Quang Minh (20227025) · Lê Thị Thu Hiền (20227109) · Nguyễn Tuấn Dũng (20227191) |
| **Ngôn ngữ** | Python 3.x |
| **Lưu trữ dữ liệu** | Tệp tin JSON (Không yêu cầu cơ sở dữ liệu ngoài) |

---

## Cấu trúc thư mục dự án

```
NhomG22_QuanLyKhoHang/
├── src/
│   ├── main.py          # Điểm khởi chạy chính — tự động chạy GUI, fallback về CLI
│   ├── gui.py           # Giao diện đồ họa người dùng (GUI) viết bằng tkinter/ttk
│   ├── models.py        # Định nghĩa các lớp dữ liệu: SanPham, GiaoDich
│   ├── storage.py       # Đọc / ghi file dữ liệu JSON và sinh mã tự động
│   ├── inventory.py     # Nghiệp vụ thêm / sửa / xóa sản phẩm, nhập & xuất kho
│   ├── search.py        # Tìm kiếm theo mã / tên / loại hàng, bộ lọc sắp xếp
│   ├── report.py        # Báo cáo nhật ký tháng, thống kê cơ cấu giá trị tồn kho
│   └── categories.py    # Quản lý danh mục loại hàng và đơn vị tính
├── data/
│   ├── products.json        # Cơ sở dữ liệu danh mục sản phẩm
│   ├── transactions.json    # Cơ sở dữ liệu nhật ký giao dịch nhập / xuất
│   └── categories.json      # Danh sách loại hàng & đơn vị tính (tự tạo khi chạy)
├── tests/
│   ├── __init__.py      # Khởi tạo gói kiểm thử
│   ├── test_models.py   # Kiểm thử lớp dữ liệu SanPham, GiaoDich
│   ├── test_storage.py  # Kiểm thử chức năng đọc/ghi file & sinh mã tự động
│   ├── test_search.py   # Kiểm thử các thuật toán sắp xếp (Bubble) & tìm kiếm (Linear)
│   ├── test_categories.py # Kiểm thử danh mục sản phẩm và đơn vị tính
│   └── test_report.py   # Kiểm thử logic tính toán báo cáo thống kê
├── run_tests.py         # Trình chạy kiểm thử tự động toàn dự án
├── requirements.txt     # Tệp khai báo các thư viện phụ thuộc Python
└── README.md
```

---

## Yêu cầu hệ thống

- **Python 3.7 trở lên**
- Thư viện xử lý ảnh `Pillow` (để hiển thị logo HUST trên giao diện GUI, nếu thiếu giao diện vẫn hoạt động bình thường nhưng tự động ẩn logo).

---

## Hướng dẫn vận hành

### 1. Chuẩn bị môi trường
Cài đặt thư viện phụ thuộc bằng lệnh sau ở thư mục gốc của dự án:
```bash
pip install -r requirements.txt
```
*(Lưu ý: Nếu không cài đặt Pillow, ứng dụng GUI vẫn khởi chạy bình thường và tự động ẩn logo trường).*

### 2. Khởi chạy ứng dụng

Khởi chạy từ thư mục gốc của dự án:

#### Khởi chạy chế độ giao diện đồ họa (GUI - Mặc định)
```bash
python src/main.py
```
*Giao diện cửa sổ trực quan hiện đại, hỗ trợ các chức năng bằng nút nhấn.*

#### Khởi chạy chế độ dòng lệnh (CLI - Console)
Nếu bạn chạy trên máy chủ không màn hình (headless) hoặc muốn sử dụng menu console truyền thống, hãy thêm tham số `--console`:
```bash
python src/main.py --console
```

### 3. Khởi chạy kiểm thử tự động (Unit Tests)
Hệ thống cung cấp một bộ kiểm thử tự động toàn diện sử dụng thư viện chuẩn `unittest` của Python để xác thực và bẫy lỗi các chức năng nghiệp vụ quan trọng.

Khởi chạy từ thư mục gốc của dự án:
```bash
python run_tests.py
```
*(Lưu ý: Bộ kiểm thử thiết lập môi trường bằng cách sử dụng các tệp tin lưu trữ tạm thời cô lập, cam kết không ghi đè hay làm ảnh hưởng đến dữ liệu thực của bạn trong thư mục data/).*

---

## Các tính năng chính & Hướng dẫn điều hướng (Menu)

### Chế độ Console (CLI) hiển thị như sau:
```
HE THONG QUAN LY KHO HANG - NHOM G22
======================================
  1. Quan ly danh muc san pham     → Quản lý danh mục sản phẩm
  2. Nhap kho / Xuat kho           → Nhập kho / Xuất kho
  3. Tim kiem san pham             → Tìm kiếm sản phẩm
  4. Bao cao & Thong ke            → Báo cáo & Thống kê
  0. Thoat chuong trinh            → Thoát
```

### 1 · Quản lý danh mục sản phẩm
| Lựa chọn | Mô tả chi tiết |
|--------|-------------|
| Hiển thị tất cả sản phẩm | Hiển thị danh mục chi tiết với lượng tồn kho và trạng thái cảnh báo |
| Thêm sản phẩm mới | Kiểm tra tính duy nhất của mã sản phẩm (chặn trùng), cảnh báo nếu trùng tên. Chọn loại hàng & đơn vị tính từ danh sách quản lý hoặc thêm mới trực tiếp. |
| Sửa thông tin sản phẩm | Chọn sản phẩm theo mã và sửa đổi từng thuộc tính (tên, đơn giá, loại hàng, đơn vị tính, ngưỡng tối thiểu). |
| Xóa sản phẩm | Chỉ cho phép xóa khi lượng tồn kho bằng 0 để tránh mất mát dữ liệu liên kết. |

### 2 · Nhập kho / Xuất kho
- **Nhập kho:** Chọn mã sản phẩm → Nhập số lượng & đơn giá nhập (có thể nhấn Enter giữ đơn giá mặc định) → Giao dịch tự động ghi nhật ký kèm ngày hôm nay.
- **Xuất kho:** Tương tự nhập kho, hệ thống kiểm tra lượng xuất có vượt quá tồn kho thực tế hay không. Nếu sau khi xuất kho lượng tồn xuống dưới hoặc bằng ngưỡng an toàn, hệ thống sẽ đưa ra cảnh báo khẩn cấp `[CANH BAO]`.

### 3 · Tìm kiếm sản phẩm
| Lựa chọn | Mô tả chi tiết |
|--------|-------------|
| Tìm theo mã sản phẩm | Khớp chính xác tuyệt đối (không phân biệt hoa/thường) |
| Tìm theo tên sản phẩm | Khớp một phần từ khóa (không phân biệt hoa/thường) |
| Tìm theo loại hàng | Khớp tương đối theo phân loại |
| Xem sản phẩm sắp hết hàng | Lọc ra các sản phẩm dưới ngưỡng tối thiểu, sắp xếp tăng dần theo lượng tồn bằng thuật toán Bubble Sort tự cài đặt. |

### 4 · Báo cáo & Thống kê
| Lựa chọn | Mô tả chi tiết |
|--------|-------------|
| Nhật ký giao dịch tháng | Hiển thị các kỳ có dữ liệu, chọn tháng/năm để in nhật ký giao dịch nhập/xuất chi tiết và tổng tiền phát sinh trong kỳ. |
| Thống kê giá trị tồn kho | Danh sách mặt hàng sắp xếp giảm dần theo giá trị tồn kho (so luong * don gia) và bảng phân tích cơ cấu tỷ trọng giá trị theo từng loại hàng. |
| Kiểm kê tổng hợp | Báo cáo nhanh: tổng số mặt hàng, tổng giá trị tồn kho, số lượng mặt hàng sắp hết hàng, tổng số giao dịch. |

---

## Tệp dữ liệu lưu trữ (JSON)

Mọi dữ liệu được lưu dưới dạng văn bản cấu trúc JSON trong thư mục `data/` và tự động cập nhật ngay sau mỗi thao tác:

| Tệp tin | Nội dung lưu trữ |
|------|----------|
| `products.json` | Danh mục sản phẩm (mã, tên, loại hàng, đơn vị tính, số lượng tồn, đơn giá, ngưỡng tối thiểu) |
| `transactions.json` | Nhật ký chi tiết giao dịch nhập/xuất kho (mã giao dịch, mã SP, loại giao dịch, số lượng, đơn giá, ngày, ghi chú) |
| `categories.json` | Danh sách loại hàng và đơn vị tính hiện có |

*Hệ thống đi kèm **10 sản phẩm mẫu và 10 giao dịch mẫu** ban đầu giúp bạn dễ dàng chạy thử nghiệm ngay lập tức.*

---

## Các lưu ý kỹ thuật

- Toàn bộ thuật toán tìm kiếm (Linear Search) và sắp xếp (Bubble Sort) đều được tự cài đặt từ đầu bằng mã nguồn gốc để tuân thủ yêu cầu môn học Kỹ thuật Lập trình tại HUST.
- Mã giao dịch (`GD0001`, `GD0002`, ...) được sinh tự động bằng cách rà soát tìm mã lớn nhất và cộng thêm 1.
- Mã sản phẩm không phân biệt chữ hoa/chữ thường và phải là duy nhất.
- Tên sản phẩm nếu nhập trùng sẽ hiển thị cảnh báo nhưng cho phép xác nhận ghi đè bằng phím nhấn.
