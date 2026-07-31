# gui.py - Giao dien do hoa (GUI) cho He Thong Quan Ly Kho Hang
# Su dung Tkinter va ttk de lam giao dien zero-dependency
# Thiet ke hien dai, ho tro Dark Mode, bo goc va tuong tac muot ma
# Nhom G22 - Chu de 3: Quan Ly Kho Hang

import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
from PIL import Image, ImageTk

# Import backend modules
from storage import (
    tai_danh_sach_san_pham, luu_danh_sach_san_pham,
    tai_danh_sach_giao_dich, them_giao_dich,
    sinh_ma_giao_dich, tim_san_pham_theo_ma,
    kiem_tra_ma_sp_ton_tai
)
from categories import tai_categories, them_loai_hang_moi, them_don_vi_tinh_moi
from search import (
    tim_kiem_theo_ma, tim_kiem_theo_ten,
    tim_kiem_theo_loai, loc_san_pham_sap_het_hang
)
from report import (
    _loc_giao_dich_theo_thang, _tinh_tong_thanh_tien,
    _sap_xep_giam_dan_gia_tri, _thong_ke_theo_loai
)
from models import SanPham, GiaoDich

# Colors Palette (Catppuccin Mocha themed dark style)
BG_MAIN = "#1e1e2e"       # Dark violet-blue background
BG_SIDEBAR = "#181825"    # Darker sidebar
BG_CARD = "#252538"       # Card/Panel background
FG_MAIN = "#cdd6f4"       # Light gray text
FG_SUB = "#a6adc8"        # Muted text
ACCENT = "#89b4fa"        # Soft blue/accent
ACCENT_GREEN = "#a6e3a1"  # Success green
ACCENT_RED = "#f38ba8"    # Warning red
ACCENT_ORANGE = "#fab387" # Warning orange
BORDER_COLOR = "#313244"  # Subtle borders

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Kho hàng - Nhóm G22")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG_MAIN)
        
        # Load and configure Custom Style
        self.setup_styles()
        
        # Main Layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Sidebar Frame
        self.sidebar = tk.Frame(self.root, bg=BG_SIDEBAR, width=220, bd=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Main Display Frame
        self.main_container = tk.Frame(self.root, bg=BG_MAIN)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Load Sidebar Header & Logo
        self.setup_sidebar()
        
        # Initialize Frames/Views
        self.frames = {}
        for view_class in (DashboardView, ProductView, TransactionView, SearchView, ReportView):
            view_name = view_class.__name__
            frame = view_class(parent=self.main_container, controller=self)
            self.frames[view_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        # Switch to Dashboard view initially
        self.show_view("DashboardView")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure common elements
        style.configure(".", background=BG_MAIN, foreground=FG_MAIN, font=("Times New Roman", 11))
        
        # Configure Treeview (Table)
        style.configure("Treeview", 
                        background=BG_CARD, 
                        foreground=FG_MAIN,
                        fieldbackground=BG_CARD,
                        rowheight=28, 
                        bd=0,
                        font=("Times New Roman", 11))
        style.map("Treeview", 
                  background=[("selected", ACCENT)], 
                  foreground=[("selected", "#11111b")])
                  
        style.configure("Treeview.Heading", 
                        background=BORDER_COLOR, 
                        foreground=FG_MAIN, 
                        relief="flat", 
                        font=("Times New Roman", 11, "bold"))
        style.map("Treeview.Heading", background=[("active", ACCENT)])
        
        # Configure Combobox
        style.configure("TCombobox", 
                        fieldbackground=BG_CARD, 
                        background=BORDER_COLOR, 
                        foreground=FG_MAIN, 
                        arrowcolor=FG_MAIN)
        
        # Scrollbars
        style.configure("TScrollbar", background=BORDER_COLOR, troughcolor=BG_MAIN, arrowcolor=FG_MAIN)

    def setup_sidebar(self):
        # 1. HUST Logo
        # Search path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_dir, "scratch", "media", "hust_logo.png")
        if not os.path.exists(logo_path):
            # Fallback path if run in current appDataDir
            logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "scratch", "media", "hust_logo.png")
            
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                # Resize keeping ratio (approx 60x88)
                img = img.resize((50, 73), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                lbl_logo = tk.Label(self.sidebar, image=self.logo_img, bg=BG_SIDEBAR)
                lbl_logo.pack(pady=(15, 5))
            except Exception as e:
                print("Failed to load logo in GUI:", e)
                
        # 2. Institution / App Header
        lbl_uni = tk.Label(self.sidebar, text="ĐẠI HỌC BÁCH KHOA HÀ NỘI", font=("Times New Roman", 9, "bold"), fg=ACCENT, bg=BG_SIDEBAR)
        lbl_uni.pack(pady=(5, 2))
        lbl_title = tk.Label(self.sidebar, text="QUẢN LÝ KHO HÀNG\nNhóm G22", font=("Times New Roman", 12, "bold"), fg=FG_MAIN, bg=BG_SIDEBAR)
        lbl_title.pack(pady=(2, 20))
        
        # 3. Sidebar Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("Tổng quan", "DashboardView"),
            ("Danh mục sản phẩm", "ProductView"),
            ("Nhập / Xuất kho", "TransactionView"),
            ("Tìm kiếm & Lọc", "SearchView"),
            ("Báo cáo & Thống kê", "ReportView")
        ]
        
        for label, view_name in nav_items:
            btn = tk.Button(self.sidebar, text=f"  {label}  ", font=("Times New Roman", 11, "bold"), 
                            bg=BG_SIDEBAR, fg=FG_SUB, activebackground=BG_CARD, activeforeground=FG_MAIN,
                            bd=0, anchor="w", cursor="hand2", padx=20, pady=10,
                            command=lambda v=view_name: self.show_view(v))
            btn.pack(fill="x", pady=2)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: self.on_btn_hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_btn_leave(b))
            
            self.nav_buttons[view_name] = btn

    def on_btn_hover(self, btn):
        if btn["fg"] != "#11111b": # If not currently active
            btn.configure(bg=BORDER_COLOR, fg=FG_MAIN)

    def on_btn_leave(self, btn):
        if btn["fg"] != "#11111b": # If not currently active
            btn.configure(bg=BG_SIDEBAR, fg=FG_SUB)

    def show_view(self, view_name):
        # Raise selected frame
        frame = self.frames[view_name]
        frame.tkraise()
        frame.on_show() # Refresh data on showing
        
        # Highlight active button
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(bg=ACCENT, fg="#11111b") # Light active background with dark text
            else:
                btn.configure(bg=BG_SIDEBAR, fg=FG_SUB)

# ============================================================
#  VIEW: DASHBOARD (TỔNG QUAN)
# ============================================================
class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        lbl_head = tk.Label(self, text="BẢNG TỔNG QUAN KHO HÀNG", font=("Times New Roman", 16, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_head.grid(row=0, column=0, columnspan=3, sticky="we", padx=25, pady=(20, 10))
        
        # Card 1: Tổng số sản phẩm
        self.card_sp = self.create_card("TỔNG SỐ MẶT HÀNG", "0", ACCENT)
        self.card_sp.grid(row=1, column=0, padx=(25, 10), pady=10, sticky="nsew")
        
        # Card 2: Tổng giá trị kho
        self.card_val = self.create_card("TỔNG GIÁ TRỊ TỒN KHO", "0 VND", ACCENT_GREEN)
        self.card_val.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Card 3: Sản phẩm sắp hết hàng
        self.card_low = self.create_card("SẢN PHẨM SẮP HẾT HÀNG", "0", ACCENT_RED)
        self.card_low.grid(row=1, column=2, padx=(10, 25), pady=10, sticky="nsew")
        
        # Bottom area (Split into low stock alert and recent transaction history)
        bottom_frame = tk.Frame(self, bg=BG_MAIN)
        bottom_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=25, pady=(10, 25))
        bottom_frame.grid_rowconfigure(1, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        # Low Stock Alert Panel
        lbl_alert = tk.Label(bottom_frame, text="CẢNH BÁO TỒN KHO (SẮP HẾT HÀNG / HẾT HÀNG)", font=("Times New Roman", 12, "bold"), fg=ACCENT_RED, bg=BG_MAIN, anchor="w")
        lbl_alert.grid(row=0, column=0, sticky="we", pady=(10, 5), padx=(0, 10))
        
        self.alert_tree = ttk.Treeview(bottom_frame, columns=("ma", "ten", "ton", "nguong"), show="headings", height=8)
        self.alert_tree.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.setup_tree_headings(self.alert_tree, [("ma", "Mã SP", 70), ("ten", "Tên sản phẩm", 180), ("ton", "Tồn kho", 80), ("nguong", "Ngưỡng cảnh báo", 120)])
        
        # Recent Transaction Panel
        lbl_trans = tk.Label(bottom_frame, text="NHẬT KÝ GIAO DỊCH GẦN ĐÂY", font=("Times New Roman", 12, "bold"), fg=ACCENT, bg=BG_MAIN, anchor="w")
        lbl_trans.grid(row=0, column=1, sticky="we", pady=(10, 5), padx=(10, 0))
        
        self.trans_tree = ttk.Treeview(bottom_frame, columns=("ma", "sp", "loai", "sl", "time"), show="headings", height=8)
        self.trans_tree.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        self.setup_tree_headings(self.trans_tree, [("ma", "Mã GD", 80), ("sp", "Sản phẩm", 160), ("loai", "Loại", 70), ("sl", "SL", 60), ("time", "Thời gian", 100)])

    def create_card(self, title, val_str, color):
        card = tk.Frame(self, bg=BG_CARD, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.grid_columnconfigure(0, weight=1)
        
        lbl_title = tk.Label(card, text=title, font=("Times New Roman", 9, "bold"), fg=FG_SUB, bg=BG_CARD)
        lbl_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        lbl_val = tk.Label(card, text=val_str, font=("Times New Roman", 16, "bold"), fg=color, bg=BG_CARD)
        lbl_val.pack(anchor="w", padx=15, pady=(0, 15))
        
        return card

    def setup_tree_headings(self, tree, cols):
        for col_id, heading, width in cols:
            tree.heading(col_id, text=heading, anchor="center")
            tree.column(col_id, width=width, anchor="center")
        
        # Tags for colors
        tree.tag_configure("red", foreground=ACCENT_RED)
        tree.tag_configure("orange", foreground=ACCENT_ORANGE)

    def on_show(self):
        # Refresh figures
        products = tai_danh_sach_san_pham()
        transactions = tai_danh_sach_giao_dich()
        
        # 1. Total products
        total_sp = len(products)
        # Update card text
        for child in self.card_sp.winfo_children():
            if child["fg"] != FG_SUB:
                child.configure(text=str(total_sp))
                
        # 2. Total value
        total_val = sum(sp.thanh_tien() for sp in products)
        for child in self.card_val.winfo_children():
            if child["fg"] != FG_SUB:
                child.configure(text=f"{total_val:,.0f} VND")
                
        # 3. Low stock count
        low_count = sum(1 for sp in products if sp.sap_het_hang())
        for child in self.card_low.winfo_children():
            if child["fg"] != FG_SUB:
                child.configure(text=str(low_count))
                
        # 4. Fill Low Stock Tree
        # Clear existing
        for item in self.alert_tree.get_children():
            self.alert_tree.delete(item)
            
        for sp in products:
            if sp.sap_het_hang():
                tag = "red" if sp.so_luong_ton == 0 else "orange"
                self.alert_tree.insert("", "end", values=(sp.ma_sp, sp.ten_sp, sp.so_luong_ton, sp.nguong_toi_thieu), tags=(tag,))
                
        # 5. Fill Recent Transactions
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
            
        # Display up to 10 latest transactions
        recent_trans = transactions[-10:]
        recent_trans.reverse() # show latest first
        for gd in recent_trans:
            loai_label = "Nhập kho" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "Xuất kho"
            tag = "orange" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "red"
            self.trans_tree.insert("", "end", values=(gd.ma_gd, f"{gd.ten_sp} ({gd.ma_sp})", loai_label, gd.so_luong, gd.ngay_thuc_hien))

# ============================================================
#  VIEW: DANH MỤC SẢN PHẨM (PRODUCT LIST)
# ============================================================
class ProductView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header & Add/Edit buttons container
        header_frame = tk.Frame(self, bg=BG_MAIN)
        header_frame.grid(row=0, column=0, sticky="we", padx=25, pady=(20, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        lbl_head = tk.Label(header_frame, text="DANH MỤC SẢN PHẨM KHO HÀNG", font=("Times New Roman", 16, "bold"), fg=FG_MAIN, bg=BG_MAIN)
        lbl_head.grid(row=0, column=0, sticky="w")
        
        btn_frame = tk.Frame(header_frame, bg=BG_MAIN)
        btn_frame.grid(row=0, column=1, sticky="e")
        
        self.btn_add = tk.Button(btn_frame, text="+ Thêm sản phẩm", font=("Times New Roman", 10, "bold"), 
                                 bg=ACCENT_GREEN, fg="#11111b", bd=0, padx=12, pady=6, cursor="hand2",
                                 command=self.open_add_dialog)
        self.btn_add.pack(side="left", padx=5)
        
        self.btn_edit = tk.Button(btn_frame, text="✎ Sửa sản phẩm", font=("Times New Roman", 10, "bold"), 
                                  bg=ACCENT, fg="#11111b", bd=0, padx=12, pady=6, cursor="hand2",
                                  command=self.open_edit_dialog)
        self.btn_edit.pack(side="left", padx=5)
        
        self.btn_delete = tk.Button(btn_frame, text="🗑 Xóa sản phẩm", font=("Times New Roman", 10, "bold"), 
                                    bg=ACCENT_RED, fg="#11111b", bd=0, padx=12, pady=6, cursor="hand2",
                                    command=self.delete_selected_product)
        self.btn_delete.pack(side="left", padx=5)
        
        # Table Frame
        tbl_frame = tk.Frame(self, bg=BG_MAIN)
        tbl_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))
        tbl_frame.grid_columnconfigure(0, weight=1)
        tbl_frame.grid_rowconfigure(0, weight=1)
        
        # Product Table (Treeview)
        cols = ("stt", "ma", "ten", "loai", "dvt", "ton", "gia", "tri", "status")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scroll.set)
        
        # Table headings and dimensions
        headings_config = [
            ("stt", "STT", 45), ("ma", "Mã SP", 75), ("ten", "Tên sản phẩm", 200),
            ("loai", "Loại hàng", 100), ("dvt", "Đơn vị tính", 80), 
            ("ton", "Số lượng tồn", 95), ("gia", "Đơn giá (VND)", 110), 
            ("tri", "Giá trị tồn (VND)", 125), ("status", "Trạng thái", 120)
        ]
        for col_id, heading, width in headings_config:
            self.tree.heading(col_id, text=heading, anchor="center")
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["stt", "ma", "dvt", "ton"] else "w" if col_id in ["ten", "loai"] else "e" if col_id in ["gia", "tri"] else "center")
            
        # Tag configuration
        self.tree.tag_configure("warn", foreground=ACCENT_ORANGE)
        self.tree.tag_configure("danger", foreground=ACCENT_RED)

    def on_show(self):
        self.refresh_table()

    def refresh_table(self):
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        products = tai_danh_sach_san_pham()
        for idx, sp in enumerate(products):
            thanh_tien = sp.thanh_tien()
            status_text = "OK"
            tag = "normal"
            if sp.so_luong_ton == 0:
                status_text = "[!] Hết hàng"
                tag = "danger"
            elif sp.sap_het_hang():
                status_text = "[!] Sắp hết hàng"
                tag = "warn"
                
            self.tree.insert("", "end", values=(
                idx + 1,
                sp.ma_sp,
                sp.ten_sp,
                sp.loai_hang,
                sp.don_vi_tinh,
                sp.so_luong_ton,
                f"{sp.don_gia:,.0f}",
                f"{thanh_tien:,.0f}",
                status_text
            ), tags=(tag,))

    def open_add_dialog(self):
        AddProductDialog(self)

    def open_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sản phẩm từ bảng để chỉnh sửa.")
            return
            
        # Get code from selected row
        ma_sp = self.tree.item(selected[0])["values"][1]
        products = tai_danh_sach_san_pham()
        sp = tim_san_pham_theo_ma(ma_sp, products)
        if sp:
            EditProductDialog(self, sp)

    def delete_selected_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sản phẩm để xóa.")
            return
            
        ma_sp = self.tree.item(selected[0])["values"][1]
        ten_sp = self.tree.item(selected[0])["values"][2]
        products = tai_danh_sach_san_pham()
        sp = tim_san_pham_theo_ma(ma_sp, products)
        
        if not sp:
            return
            
        # Specification Constraint check: Can only delete if stock is 0
        if sp.so_luong_ton > 0:
            messagebox.showerror("Lỗi nghiệp vụ", f"Không thể xóa sản phẩm '{ten_sp}' vì số lượng tồn kho hiện tại là {sp.so_luong_ton}.\n\nYêu cầu nghiệp vụ: Chỉ cho phép xóa khi số lượng tồn bằng 0.")
            return
            
        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa sản phẩm '{ten_sp}' ({ma_sp}) khỏi danh mục không?")
        if confirm:
            # Delete from array
            new_list = [item for item in products if item.ma_sp != ma_sp]
            if luu_danh_sach_san_pham(new_list):
                messagebox.showinfo("Thành công", f"Đã xóa sản phẩm '{ten_sp}' thành công.")
                self.refresh_table()
            else:
                messagebox.showerror("Lỗi", "Không thể lưu tệp dữ liệu sau khi xóa.")

# ============================================================
#  DIALOG: THÊM SẢN PHẨM MỚI (ADD PRODUCT DIALOG)
# ============================================================
class AddProductDialog(tk.Toplevel):
    def __init__(self, parent_view):
        super().__init__(parent_view, bg=BG_CARD)
        self.parent_view = parent_view
        self.title("Thêm sản phẩm mới")
        self.geometry("450x450")
        self.resizable(False, False)
        
        # Center in parent window
        self.transient(parent_view.master)
        self.grab_set()
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # Load categories list
        self.cats = tai_categories()
        
        lbl_head = tk.Label(self, text="THÔNG TIN SẢN PHẨM MỚI", font=("Times New Roman", 13, "bold"), fg=ACCENT, bg=BG_CARD)
        lbl_head.grid(row=0, column=0, columnspan=2, pady=15)
        
        # Fields Configuration
        self.entries = {}
        fields = [
            ("ma_sp", "Mã sản phẩm (*):", "Entry", None),
            ("ten_sp", "Tên sản phẩm (*):", "Entry", None),
            ("loai_hang", "Loại hàng (*):", "Combobox", self.cats["loai_hang"]),
            ("don_vi_tinh", "Đơn vị tính (*):", "Combobox", self.cats["don_vi_tinh"]),
            ("so_luong_ton", "Số lượng ban đầu (*):", "Entry", "0"),
            ("don_gia", "Đơn giá (VND) (*):", "Entry", None),
            ("nguong_toi_thieu", "Ngưỡng cảnh báo (*):", "Entry", "10")
        ]
        
        for idx, (key, label, w_type, vals) in enumerate(fields):
            lbl = tk.Label(self, text=label, font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
            lbl.grid(row=idx+1, column=0, sticky="we", padx=(20, 10), pady=8)
            
            if w_type == "Entry":
                ent = tk.Entry(self, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
                if vals:
                    ent.insert(0, vals)
                ent.grid(row=idx+1, column=1, sticky="we", padx=(10, 20), pady=8)
                self.entries[key] = ent
            else:
                cbo = ttk.Combobox(self, values=vals, font=("Times New Roman", 10), state="readonly")
                cbo.grid(row=idx+1, column=1, sticky="we", padx=(10, 20), pady=8)
                if vals:
                    cbo.set(vals[0])
                self.entries[key] = cbo
                
        # Buttons
        btn_frame = tk.Frame(self, bg=BG_CARD)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        btn_save = tk.Button(btn_frame, text=" Lưu lại ", font=("Times New Roman", 10, "bold"), bg=ACCENT_GREEN, fg="#11111b", bd=0, padx=15, pady=6, cursor="hand2", command=self.save_product)
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = tk.Button(btn_frame, text=" Hủy bỏ ", font=("Times New Roman", 10, "bold"), bg=BORDER_COLOR, fg=FG_MAIN, bd=0, padx=15, pady=6, cursor="hand2", command=self.destroy)
        btn_cancel.pack(side="left", padx=10)

    def save_product(self):
        # Validate data
        ma_sp = self.entries["ma_sp"].get().strip().upper()
        ten_sp = self.entries["ten_sp"].get().strip()
        loai_hang = self.entries["loai_hang"].get()
        don_vi_tinh = self.entries["don_vi_tinh"].get()
        
        # Safe checks
        if not ma_sp or not ten_sp:
            messagebox.showerror("Lỗi nhập liệu", "Mã và Tên sản phẩm không được để trống!")
            return
            
        # Clean garbage characters
        ma_sp = "".join(ma_sp.split())
        for char in ['"', "'", '\\', '/', '*', '?', '[', ']']:
            ma_sp = ma_sp.replace(char, "")
            ten_sp = ten_sp.replace(char, "")
        ten_sp = " ".join(ten_sp.split())
        
        if not ma_sp or not ten_sp:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập mã và tên hợp lệ (chữ và số, không chứa kí tự đặc biệt).")
            return
            
        products = tai_danh_sach_san_pham()
        if kiem_tra_ma_sp_ton_tai(ma_sp, products):
            messagebox.showerror("Lỗi trùng lặp", f"Mã sản phẩm '{ma_sp}' đã tồn tại trong danh mục hệ thống!")
            return
            
        # Check duplicate name (warning but allow proceed)
        ten_trung = False
        for p in products:
            if p.ten_sp.lower() == ten_sp.lower():
                ten_trung = True
                break
        if ten_trung:
            confirm = messagebox.askyesno("Cảnh báo", f"Tên sản phẩm '{ten_sp}' đã trùng với một sản phẩm khác có sẵn. Bạn có chắc muốn tạo sản phẩm mới cùng tên?")
            if not confirm:
                return
                
        # Parse integers and numbers
        try:
            so_luong_ton = int(self.entries["so_luong_ton"].get().strip())
            don_gia = float(self.entries["don_gia"].get().strip())
            nguong_toi_thieu = int(self.entries["nguong_toi_thieu"].get().strip())
            
            if so_luong_ton < 0 or don_gia <= 0 or nguong_toi_thieu < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi kiểu dữ liệu", "Số lượng, Đơn giá và Ngưỡng tối thiểu phải là số nguyên dương lớn hơn 0!")
            return
            
        # Create object
        new_sp = SanPham(ma_sp, ten_sp, loai_hang, don_vi_tinh, so_luong_ton, don_gia, nguong_toi_thieu)
        products.append(new_sp)
        
        if luu_danh_sach_san_pham(products):
            messagebox.showinfo("Thành công", f"Đã thêm sản phẩm '{ten_sp}' vào danh mục thành công!")
            self.parent_view.refresh_table()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu tệp dữ liệu.")

# ============================================================
#  DIALOG: CHỈNH SỬA THÔNG TIN SẢN PHẨM (EDIT DIALOG)
# ============================================================
class EditProductDialog(tk.Toplevel):
    def __init__(self, parent_view, product):
        super().__init__(parent_view, bg=BG_CARD)
        self.parent_view = parent_view
        self.product = product
        self.title("Chỉnh sửa thông tin sản phẩm")
        self.geometry("450x420")
        self.resizable(False, False)
        
        self.transient(parent_view.master)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.cats = tai_categories()
        
        lbl_head = tk.Label(self, text=f"SỬA SẢN PHẨM: {product.ma_sp}", font=("Times New Roman", 13, "bold"), fg=ACCENT, bg=BG_CARD)
        lbl_head.grid(row=0, column=0, columnspan=2, pady=15)
        
        # Fields Configuration
        self.entries = {}
        fields = [
            ("ten_sp", "Tên sản phẩm (*):", "Entry", product.ten_sp),
            ("loai_hang", "Loại hàng (*):", "Combobox", self.cats["loai_hang"]),
            ("don_vi_tinh", "Đơn vị tính (*):", "Combobox", self.cats["don_vi_tinh"]),
            ("don_gia", "Đơn giá (VND) (*):", "Entry", str(int(product.don_gia))),
            ("nguong_toi_thieu", "Ngưỡng cảnh báo (*):", "Entry", str(product.nguong_toi_thieu))
        ]
        
        for idx, (key, label, w_type, val) in enumerate(fields):
            lbl = tk.Label(self, text=label, font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
            lbl.grid(row=idx+1, column=0, sticky="we", padx=(20, 10), pady=10)
            
            if w_type == "Entry":
                ent = tk.Entry(self, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
                ent.insert(0, val)
                ent.grid(row=idx+1, column=1, sticky="we", padx=(10, 20), pady=10)
                self.entries[key] = ent
            else:
                cbo = ttk.Combobox(self, values=val, font=("Times New Roman", 10), state="readonly")
                cbo.grid(row=idx+1, column=1, sticky="we", padx=(10, 20), pady=10)
                cbo.set(val[0] if val else "")
                if product.__dict__[key] in val:
                    cbo.set(product.__dict__[key])
                self.entries[key] = cbo
                
        # Buttons
        btn_frame = tk.Frame(self, bg=BG_CARD)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        btn_save = tk.Button(btn_frame, text=" Cập nhật ", font=("Times New Roman", 10, "bold"), bg=ACCENT_GREEN, fg="#11111b", bd=0, padx=15, pady=6, cursor="hand2", command=self.update_product)
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = tk.Button(btn_frame, text=" Hủy bỏ ", font=("Times New Roman", 10, "bold"), bg=BORDER_COLOR, fg=FG_MAIN, bd=0, padx=15, pady=6, cursor="hand2", command=self.destroy)
        btn_cancel.pack(side="left", padx=10)

    def update_product(self):
        # Validate data
        ten_sp = self.entries["ten_sp"].get().strip()
        loai_hang = self.entries["loai_hang"].get()
        don_vi_tinh = self.entries["don_vi_tinh"].get()
        
        if not ten_sp:
            messagebox.showerror("Lỗi nhập liệu", "Tên sản phẩm không được để trống!")
            return
            
        # Clean garbage characters
        for char in ['"', "'", '\\', '/', '*', '?', '[', ']']:
            ten_sp = ten_sp.replace(char, "")
        ten_sp = " ".join(ten_sp.split())
        
        if not ten_sp:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập tên sản phẩm hợp lệ.")
            return
            
        products = tai_danh_sach_san_pham()
        
        # Check duplicate name with OTHER products
        ten_trung = False
        for p in products:
            if p.ma_sp != self.product.ma_sp and p.ten_sp.lower() == ten_sp.lower():
                ten_trung = True
                break
        if ten_trung:
            confirm = messagebox.askyesno("Cảnh báo", f"Tên sản phẩm '{ten_sp}' trùng với sản phẩm khác. Bạn vẫn muốn cập nhật?")
            if not confirm:
                return
                
        # Parse integers and numbers
        try:
            don_gia = float(self.entries["don_gia"].get().strip())
            nguong_toi_thieu = int(self.entries["nguong_toi_thieu"].get().strip())
            
            if don_gia <= 0 or nguong_toi_thieu < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi kiểu dữ liệu", "Đơn giá và Ngưỡng tối thiểu phải là số nguyên dương lớn hơn 0!")
            return
            
        # Update object inside loaded array
        for sp in products:
            if sp.ma_sp == self.product.ma_sp:
                sp.ten_sp = ten_sp
                sp.loai_hang = loai_hang
                sp.don_vi_tinh = don_vi_tinh
                sp.don_gia = don_gia
                sp.nguong_toi_thieu = nguong_toi_thieu
                break
                
        if luu_danh_sach_san_pham(products):
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin sản phẩm '{self.product.ma_sp}' thành công!")
            self.parent_view.refresh_table()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu tệp dữ liệu.")

# ============================================================
#  VIEW: NHẬP KHO / XUẤT KHO (TRANSACTION VIEW)
# ============================================================
class TransactionView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)
        
        # Left Side: Recent Transactions History
        history_frame = tk.Frame(self, bg=BG_MAIN)
        history_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(25, 10), pady=20)
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1)
        
        lbl_hist_title = tk.Label(history_frame, text="LỊCH SỬ GIAO DỊCH TRONG KHO", font=("Times New Roman", 13, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_hist_title.grid(row=0, column=0, pady=(0, 10), sticky="we")
        
        self.hist_tree = ttk.Treeview(history_frame, columns=("ma", "sp", "loai", "sl", "dongia", "time"), show="headings")
        self.hist_tree.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        scr = ttk.Scrollbar(history_frame, orient="vertical", command=self.hist_tree.yview)
        scr.grid(row=1, column=1, sticky="ns")
        self.hist_tree.configure(yscrollcommand=scr.set)
        
        self.hist_tree.heading("ma", text="Mã GD", anchor="center")
        self.hist_tree.column("ma", width=75, anchor="center")
        self.hist_tree.heading("sp", text="Sản phẩm", anchor="center")
        self.hist_tree.column("sp", width=140, anchor="w")
        self.hist_tree.heading("loai", text="Loại", anchor="center")
        self.hist_tree.column("loai", width=70, anchor="center")
        self.hist_tree.heading("sl", text="SL", anchor="center")
        self.hist_tree.column("sl", width=50, anchor="center")
        self.hist_tree.heading("dongia", text="Đơn giá (VND)", anchor="center")
        self.hist_tree.column("dongia", width=95, anchor="e")
        self.hist_tree.heading("time", text="Ngày thực hiện", anchor="center")
        self.hist_tree.column("time", width=95, anchor="center")
        
        self.hist_tree.tag_configure("nhap", foreground=ACCENT_GREEN)
        self.hist_tree.tag_configure("xuat", foreground=ACCENT_RED)
        
        # Right Side: Transaction Form Panel
        form_frame = tk.Frame(self, bg=BG_CARD, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        form_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 25), pady=20)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)
        
        lbl_form_title = tk.Label(form_frame, text="THỰC HIỆN GIAO DỊCH KHO", font=("Times New Roman", 13, "bold"), fg=ACCENT, bg=BG_CARD)
        lbl_form_title.grid(row=0, column=0, columnspan=2, pady=15)
        
        # Product selector
        lbl_sp = tk.Label(form_frame, text="Sản phẩm (*):", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
        lbl_sp.grid(row=1, column=0, padx=(15, 5), pady=12, sticky="we")
        
        self.cbo_sp = ttk.Combobox(form_frame, font=("Times New Roman", 10), state="readonly")
        self.cbo_sp.grid(row=1, column=1, padx=(5, 15), pady=12, sticky="we")
        self.cbo_sp.bind("<<ComboboxSelected>>", self.on_product_selected)
        
        # Type
        lbl_type = tk.Label(form_frame, text="Giao dịch (*):", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
        lbl_type.grid(row=2, column=0, padx=(15, 5), pady=12, sticky="we")
        
        self.cbo_type = ttk.Combobox(form_frame, values=["Nhập kho", "Xuất kho"], font=("Times New Roman", 10), state="readonly")
        self.cbo_type.grid(row=2, column=1, padx=(5, 15), pady=12, sticky="we")
        self.cbo_type.set("Nhập kho")
        
        # Quantity
        lbl_qty = tk.Label(form_frame, text="Số lượng (*):", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
        lbl_qty.grid(row=3, column=0, padx=(15, 5), pady=12, sticky="we")
        
        self.ent_qty = tk.Entry(form_frame, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.ent_qty.grid(row=3, column=1, padx=(5, 15), pady=12, sticky="we")
        
        # Price
        lbl_price = tk.Label(form_frame, text="Đơn giá giao dịch:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
        lbl_price.grid(row=4, column=0, padx=(15, 5), pady=12, sticky="we")
        
        self.ent_price = tk.Entry(form_frame, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.ent_price.grid(row=4, column=1, padx=(5, 15), pady=12, sticky="we")
        
        # Note
        lbl_note = tk.Label(form_frame, text="Ghi chú:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD, anchor="e")
        lbl_note.grid(row=5, column=0, padx=(15, 5), pady=12, sticky="we")
        
        self.ent_note = tk.Entry(form_frame, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.ent_note.grid(row=5, column=1, padx=(5, 15), pady=12, sticky="we")
        
        # Submit Button
        btn_submit = tk.Button(form_frame, text=" Thực hiện giao dịch ", font=("Times New Roman", 11, "bold"), 
                               bg=ACCENT, fg="#11111b", bd=0, padx=20, pady=8, cursor="hand2",
                               command=self.submit_transaction)
        btn_submit.grid(row=6, column=0, columnspan=2, pady=25)

    def on_show(self):
        # Refresh product dropdown
        self.products = tai_danh_sach_san_pham()
        cbo_vals = []
        for p in self.products:
            cbo_vals.append(f"{p.ma_sp} - {p.ten_sp} (Tồn: {p.so_luong_ton})")
        self.cbo_sp.configure(values=cbo_vals)
        if cbo_vals:
            self.cbo_sp.set(cbo_vals[0])
            self.on_product_selected(None)
            
        # Refresh log table
        self.refresh_transactions_table()

    def on_product_selected(self, event):
        sel = self.cbo_sp.get()
        if not sel:
            return
        ma_sp = sel.split(" - ")[0]
        sp = tim_san_pham_theo_ma(ma_sp, self.products)
        if sp:
            self.ent_price.delete(0, tk.END)
            self.ent_price.insert(0, str(int(sp.don_gia)))

    def refresh_transactions_table(self):
        for item in self.hist_tree.get_children():
            self.hist_tree.delete(item)
            
        transactions = tai_danh_sach_giao_dich()
        recent = list(transactions[-20:])
        recent.reverse() # show latest first
        
        for gd in recent:
            loai_lbl = "Nhập" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "Xuất"
            tag = "nhap" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "xuat"
            self.hist_tree.insert("", "end", values=(
                gd.ma_gd,
                f"{gd.ten_sp} ({gd.ma_sp})",
                loai_lbl,
                gd.so_luong,
                f"{gd.don_gia:,.0f}",
                gd.ngay_thuc_hien
            ), tags=(tag,))

    def submit_transaction(self):
        sel_sp = self.cbo_sp.get()
        if not sel_sp:
            messagebox.showerror("Lỗi", "Vui lòng tạo sản phẩm trước khi thực hiện giao dịch!")
            return
            
        ma_sp = sel_sp.split(" - ")[0]
        sp = tim_san_pham_theo_ma(ma_sp, self.products)
        if not sp:
            return
            
        loai_hang = self.cbo_type.get()
        loai_giao_dich = GiaoDich.LOAI_NHAP if loai_hang == "Nhập kho" else GiaoDich.LOAI_XUAT
        
        # Validate quantity
        try:
            so_luong = int(self.ent_qty.get().strip())
            if so_luong <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng giao dịch phải là số nguyên lớn hơn 0!")
            return
            
        # Validate price
        try:
            don_gia = float(self.ent_price.get().strip())
            if don_gia <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Đơn giá giao dịch phải là số nguyên dương lớn hơn 0!")
            return
            
        ghi_chu = self.ent_note.get().strip()
        # Clean note string
        for char in ['"', "'", '\\']:
            ghi_chu = ghi_chu.replace(char, "")
            
        # Business logic checks
        if loai_giao_dich == GiaoDich.LOAI_XUAT:
            if sp.so_luong_ton < so_luong:
                messagebox.showerror("Lỗi xuất kho", f"Số lượng tồn kho không đủ để xuất!\n\nSố lượng trong kho: {sp.so_luong_ton}\nSố lượng yêu cầu xuất: {so_luong}")
                return
            sp.so_luong_ton -= so_luong
        else:
            sp.so_luong_ton += so_luong
            
        # Update product's current unit price to match transaction price
        sp.don_gia = don_gia
        
        # Save product updates
        if not luu_danh_sach_san_pham(self.products):
            messagebox.showerror("Lỗi", "Không thể lưu tệp sản phẩm.")
            return
            
        # Auto-generate Transaction ID
        ma_gd = sinh_ma_giao_dich()
        ngay_hom_nay = datetime.date.today().strftime("%Y-%m-%d")
        
        new_gd = GiaoDich(ma_gd, ma_sp, sp.ten_sp, loai_giao_dich, so_luong, don_gia, ngay_hom_nay, ghi_chu)
        
        if them_giao_dich(new_gd):
            # Warning checks
            low_stock_msg = ""
            if sp.sap_het_hang():
                low_stock_msg = f"\n\n[!] CẢNH BÁO: Sản phẩm '{sp.ten_sp}' đã đạt mức cảnh báo tối thiểu! (Tồn kho: {sp.so_luong_ton} <= Ngưỡng: {sp.nguong_toi_thieu})"
            
            messagebox.showinfo("Thành công", f"Đã thực hiện giao dịch {loai_hang.lower()} thành công! Mã GD: {ma_gd}{low_stock_msg}")
            
            # Reset fields
            self.ent_qty.delete(0, tk.END)
            self.ent_note.delete(0, tk.END)
            
            # Refresh view
            self.on_show()
        else:
            messagebox.showerror("Lỗi", "Không thể lưu giao dịch.")

# ============================================================
#  VIEW: TÌM KIẾM & LỌC SẢN PHẨM (SEARCH VIEW)
# ============================================================
class SearchView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        lbl_head = tk.Label(self, text="TÌM KIẾM VÀ LỌC SẢN PHẨM", font=("Times New Roman", 16, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_head.grid(row=0, column=0, sticky="we", padx=25, pady=(20, 10))
        
        # Control Search Box Panel
        ctrl_frame = tk.Frame(self, bg=BG_CARD, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        ctrl_frame.grid(row=1, column=0, sticky="we", padx=25, pady=10)
        
        # Columns sizing
        ctrl_frame.grid_columnconfigure(1, weight=1)
        
        lbl_type = tk.Label(ctrl_frame, text="Tìm kiếm theo:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD)
        lbl_type.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="w")
        
        self.cbo_search_type = ttk.Combobox(ctrl_frame, values=["Tên sản phẩm", "Mã sản phẩm", "Loại hàng", "Canh báo hết hàng"], font=("Times New Roman", 10), state="readonly", width=18)
        self.cbo_search_type.grid(row=0, column=1, padx=5, pady=15, sticky="w")
        self.cbo_search_type.set("Tên sản phẩm")
        self.cbo_search_type.bind("<<ComboboxSelected>>", self.on_search_type_changed)
        
        self.lbl_keyword = tk.Label(ctrl_frame, text="Từ khóa:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD)
        self.lbl_keyword.grid(row=0, column=2, padx=5, pady=15, sticky="w")
        
        self.ent_keyword = tk.Entry(ctrl_frame, font=("Times New Roman", 10), bg=BG_MAIN, fg=FG_MAIN, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1, width=28)
        self.ent_keyword.grid(row=0, column=3, padx=5, pady=15, sticky="w")
        self.ent_keyword.bind("<KeyRelease>", lambda e: self.perform_search())
        
        btn_search = tk.Button(ctrl_frame, text=" Tìm kiếm ", font=("Times New Roman", 10, "bold"), bg=ACCENT, fg="#11111b", bd=0, padx=15, pady=5, cursor="hand2", command=self.perform_search)
        btn_search.grid(row=0, column=4, padx=(5, 15), pady=15, sticky="e")
        
        # Results Table Frame
        tbl_frame = tk.Frame(self, bg=BG_MAIN)
        tbl_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=(10, 25))
        tbl_frame.grid_columnconfigure(0, weight=1)
        tbl_frame.grid_rowconfigure(0, weight=1)
        
        cols = ("stt", "ma", "ten", "loai", "dvt", "ton", "gia", "tri", "status")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        v_scroll = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scroll.set)
        
        # Table headings and dimensions
        headings_config = [
            ("stt", "STT", 45), ("ma", "Mã SP", 75), ("ten", "Tên sản phẩm", 220),
            ("loai", "Loại hàng", 100), ("dvt", "ĐVT", 65), 
            ("ton", "Số tồn", 75), ("gia", "Đơn giá (VND)", 110), 
            ("tri", "Giá trị tồn (VND)", 125), ("status", "Trạng thái", 120)
        ]
        for col_id, heading, width in headings_config:
            self.tree.heading(col_id, text=heading, anchor="center")
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["stt", "ma", "dvt", "ton"] else "w" if col_id in ["ten", "loai"] else "e" if col_id in ["gia", "tri"] else "center")
            
        self.tree.tag_configure("warn", foreground=ACCENT_ORANGE)
        self.tree.tag_configure("danger", foreground=ACCENT_RED)

    def on_show(self):
        self.perform_search()

    def on_search_type_changed(self, event):
        s_type = self.cbo_search_type.get()
        if s_type == "Canh báo hết hàng":
            self.ent_keyword.delete(0, tk.END)
            self.ent_keyword.configure(state="disabled")
        else:
            self.ent_keyword.configure(state="normal")
        self.perform_search()

    def perform_search(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        products = tai_danh_sach_san_pham()
        s_type = self.cbo_search_type.get()
        keyword = self.ent_keyword.get().strip()
        
        results = []
        
        # Apply compliant backend algorithms
        if s_type == "Tên sản phẩm":
            results = tim_kiem_theo_ten(keyword, products)
        elif s_type == "Mã sản phẩm":
            results = tim_kiem_theo_ma(keyword, products)
        elif s_type == "Loại hàng":
            results = tim_kiem_theo_loai(keyword, products)
        elif s_type == "Canh báo hết hàng":
            results = loc_san_pham_sap_het_hang(products)
            
        # Display results
        for idx, sp in enumerate(results):
            thanh_tien = sp.thanh_tien()
            status_text = "OK"
            tag = "normal"
            if sp.so_luong_ton == 0:
                status_text = "[!] Hết hàng"
                tag = "danger"
            elif sp.sap_het_hang():
                status_text = "[!] Sắp hết hàng"
                tag = "warn"
                
            self.tree.insert("", "end", values=(
                idx + 1,
                sp.ma_sp,
                sp.ten_sp,
                sp.loai_hang,
                sp.don_vi_tinh,
                sp.so_luong_ton,
                f"{sp.don_gia:,.0f}",
                f"{thanh_tien:,.0f}",
                status_text
            ), tags=(tag,))

# ============================================================
#  VIEW: BÁO CÁO & THỐNG KÊ (REPORT VIEW)
# ============================================================
class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_MAIN)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        lbl_head = tk.Label(self, text="BẢNG BÁO CÁO & THỐNG KÊ", font=("Times New Roman", 16, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_head.grid(row=0, column=0, sticky="we", padx=25, pady=(20, 10))
        
        # Tabbed Control Notebook for Report types
        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))
        
        # Sub-tab 1: Báo cáo tháng
        self.tab_month = tk.Frame(notebook, bg=BG_MAIN)
        notebook.add(self.tab_month, text="  Báo cáo giao dịch theo tháng  ")
        self.setup_month_report_view()
        
        # Sub-tab 2: Thống kê cơ cấu tồn kho
        self.tab_stock = tk.Frame(notebook, bg=BG_MAIN)
        notebook.add(self.tab_stock, text="  Thống kê giá trị tồn kho  ")
        self.setup_stock_report_view()

    def setup_month_report_view(self):
        self.tab_month.grid_columnconfigure(0, weight=1)
        self.tab_month.grid_rowconfigure(2, weight=1)
        
        # Filter Month/Year box
        ctrl_frame = tk.Frame(self.tab_month, bg=BG_CARD, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        ctrl_frame.grid(row=0, column=0, sticky="we", padx=15, pady=10)
        
        lbl_m = tk.Label(ctrl_frame, text="Chọn Tháng:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD)
        lbl_m.grid(row=0, column=0, padx=(15, 5), pady=15)
        
        months_arr = [f"{m:02d}" for m in range(1, 13)]
        self.cbo_m = ttk.Combobox(ctrl_frame, values=months_arr, font=("Times New Roman", 10), state="readonly", width=8)
        self.cbo_m.grid(row=0, column=1, padx=5, pady=15)
        self.cbo_m.set(f"{datetime.date.today().month:02d}")
        
        lbl_y = tk.Label(ctrl_frame, text="Năm:", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_CARD)
        lbl_y.grid(row=0, column=2, padx=5, pady=15)
        
        years_arr = [str(y) for y in range(2020, 2031)]
        self.cbo_y = ttk.Combobox(ctrl_frame, values=years_arr, font=("Times New Roman", 10), state="readonly", width=8)
        self.cbo_y.grid(row=0, column=3, padx=5, pady=15)
        self.cbo_y.set(str(datetime.date.today().year))
        
        btn_gen = tk.Button(ctrl_frame, text=" Xuất báo cáo tháng ", font=("Times New Roman", 10, "bold"), bg=ACCENT, fg="#11111b", bd=0, padx=15, pady=5, cursor="hand2", command=self.generate_month_report)
        btn_gen.grid(row=0, column=4, padx=(15, 15), pady=15)
        
        # Summary Box
        self.summary_frame = tk.Frame(self.tab_month, bg=BG_CARD, bd=1, relief="flat", highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.summary_frame.grid(row=1, column=0, sticky="we", padx=15, pady=5)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(2, weight=1)
        
        self.lbl_sum_nhap = tk.Label(self.summary_frame, text="Tổng tiền nhập: 0 VND", font=("Times New Roman", 11, "bold"), fg=ACCENT_GREEN, bg=BG_CARD)
        self.lbl_sum_nhap.grid(row=0, column=0, pady=12)
        
        self.lbl_sum_xuat = tk.Label(self.summary_frame, text="Tổng tiền xuất: 0 VND", font=("Times New Roman", 11, "bold"), fg=ACCENT_RED, bg=BG_CARD)
        self.lbl_sum_xuat.grid(row=0, column=1, pady=12)
        
        self.lbl_sum_gd = tk.Label(self.summary_frame, text="Số lượng giao dịch: 0", font=("Times New Roman", 11, "bold"), fg=FG_MAIN, bg=BG_CARD)
        self.lbl_sum_gd.grid(row=0, column=2, pady=12)
        
        # Transactions table in Month
        tbl_frame = tk.Frame(self.tab_month, bg=BG_MAIN)
        tbl_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
        tbl_frame.grid_columnconfigure(0, weight=1)
        tbl_frame.grid_rowconfigure(0, weight=1)
        
        cols = ("ma", "sp", "loai", "sl", "dongia", "tri", "time", "note")
        self.month_tree = ttk.Treeview(tbl_frame, columns=cols, show="headings")
        self.month_tree.grid(row=0, column=0, sticky="nsew")
        
        scr = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.month_tree.yview)
        scr.grid(row=0, column=1, sticky="ns")
        self.month_tree.configure(yscrollcommand=scr.set)
        
        self.month_tree.heading("ma", text="Mã GD", anchor="center")
        self.month_tree.column("ma", width=75, anchor="center")
        self.month_tree.heading("sp", text="Sản phẩm", anchor="center")
        self.month_tree.column("sp", width=140, anchor="w")
        self.month_tree.heading("loai", text="Loại GD", anchor="center")
        self.month_tree.column("loai", width=75, anchor="center")
        self.month_tree.heading("sl", text="Số lượng", anchor="center")
        self.month_tree.column("sl", width=65, anchor="center")
        self.month_tree.heading("dongia", text="Đơn giá", anchor="center")
        self.month_tree.column("dongia", width=95, anchor="e")
        self.month_tree.heading("tri", text="Thành tiền", anchor="center")
        self.month_tree.column("tri", width=110, anchor="e")
        self.month_tree.heading("time", text="Ngày thực hiện", anchor="center")
        self.month_tree.column("time", width=95, anchor="center")
        self.month_tree.heading("note", text="Ghi chú", anchor="center")
        self.month_tree.column("note", width=120, anchor="w")
        
        self.month_tree.tag_configure("nhap", foreground=ACCENT_GREEN)
        self.month_tree.tag_configure("xuat", foreground=ACCENT_RED)

    def setup_stock_report_view(self):
        self.tab_stock.grid_columnconfigure(0, weight=1)
        self.tab_stock.grid_columnconfigure(1, weight=1)
        self.tab_stock.grid_rowconfigure(1, weight=1)
        
        # Header / buttons
        btn_frame = tk.Frame(self.tab_stock, bg=BG_MAIN)
        btn_frame.grid(row=0, column=0, columnspan=2, sticky="we", padx=15, pady=10)
        
        lbl_st_title = tk.Label(btn_frame, text="THỐNG KÊ CHI TIẾT TỒN KHO THEO GIÁ TRỊ VÀ LOẠI HÀNG", font=("Times New Roman", 12, "bold"), fg=ACCENT, bg=BG_MAIN)
        lbl_st_title.pack(side="left")
        
        btn_st_run = tk.Button(btn_frame, text=" Chạy thống kê cơ cấu ", font=("Times New Roman", 10, "bold"), bg=ACCENT_GREEN, fg="#11111b", bd=0, padx=15, pady=5, cursor="hand2", command=self.generate_stock_stats)
        btn_st_run.pack(side="right")
        
        # Left Side Table: Value of each product (Sorted Descending)
        left_frame = tk.Frame(self.tab_stock, bg=BG_MAIN)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 10), pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        
        lbl_left = tk.Label(left_frame, text="GIÁ TRỊ TỒN KHO GIẢM DẦN", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_left.grid(row=0, column=0, sticky="we", pady=(0, 5))
        
        self.stock_val_tree = ttk.Treeview(left_frame, columns=("ma", "ten", "loai", "ton", "gia", "tri"), show="headings")
        self.stock_val_tree.grid(row=1, column=0, sticky="nsew")
        
        scr_l = ttk.Scrollbar(left_frame, orient="vertical", command=self.stock_val_tree.yview)
        scr_l.grid(row=1, column=1, sticky="ns")
        self.stock_val_tree.configure(yscrollcommand=scr_l.set)
        
        self.stock_val_tree.heading("ma", text="Mã SP", anchor="center")
        self.stock_val_tree.column("ma", width=70, anchor="center")
        self.stock_val_tree.heading("ten", text="Tên sản phẩm", anchor="center")
        self.stock_val_tree.column("ten", width=140, anchor="w")
        self.stock_val_tree.heading("loai", text="Loại hàng", anchor="center")
        self.stock_val_tree.column("loai", width=85, anchor="w")
        self.stock_val_tree.heading("ton", text="Tồn", anchor="center")
        self.stock_val_tree.column("ton", width=50, anchor="center")
        self.stock_val_tree.heading("gia", text="Đơn giá", anchor="center")
        self.stock_val_tree.column("gia", width=85, anchor="e")
        self.stock_val_tree.heading("tri", text="Giá trị tồn (VND)", anchor="center")
        self.stock_val_tree.column("tri", width=105, anchor="e")
        
        # Right Side Table: Category Group values and ratios
        right_frame = tk.Frame(self.tab_stock, bg=BG_MAIN)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 15), pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        lbl_right = tk.Label(right_frame, text="CƠ CẤU PHÂN BỔ THEO LOẠI HÀNG", font=("Times New Roman", 10, "bold"), fg=FG_MAIN, bg=BG_MAIN, anchor="w")
        lbl_right.grid(row=0, column=0, sticky="we", pady=(0, 5))
        
        self.cat_stats_tree = ttk.Treeview(right_frame, columns=("loai", "sl", "tri", "ratio"), show="headings")
        self.cat_stats_tree.grid(row=1, column=0, sticky="nsew")
        
        scr_r = ttk.Scrollbar(right_frame, orient="vertical", command=self.cat_stats_tree.yview)
        scr_r.grid(row=1, column=1, sticky="ns")
        self.cat_stats_tree.configure(yscrollcommand=scr_r.set)
        
        self.cat_stats_tree.heading("loai", text="Loại sản phẩm", anchor="center")
        self.cat_stats_tree.column("loai", width=130, anchor="w")
        self.cat_stats_tree.heading("sl", text="Số mã hàng", anchor="center")
        self.cat_stats_tree.column("sl", width=90, anchor="center")
        self.cat_stats_tree.heading("tri", text="Tổng giá trị tồn (VND)", anchor="center")
        self.cat_stats_tree.column("tri", width=130, anchor="e")
        self.cat_stats_tree.heading("ratio", text="Tỉ lệ %", anchor="center")
        self.cat_stats_tree.column("ratio", width=70, anchor="center")

    def on_show(self):
        # Auto-refresh reports
        self.generate_month_report()
        self.generate_stock_stats()

    def generate_month_report(self):
        month = self.cbo_m.get()
        year = self.cbo_y.get()
        
        if not month or not year:
            return
            
        prefix = f"{year}-{month}"
        
        # Fetch transaction list
        all_trans = tai_danh_sach_giao_dich()
        filtered = _loc_giao_dich_theo_thang(all_trans, prefix)
        
        # Calculate statistics using compliant code logic
        count_gd = len(filtered)
        
        sum_nhap = 0
        sum_xuat = 0
        for gd in filtered:
            if gd.loai_giao_dich == GiaoDich.LOAI_NHAP:
                sum_nhap += gd.thanh_tien()
            else:
                sum_xuat += gd.thanh_tien()
                
        # Update summary labels
        self.lbl_sum_nhap.configure(text=f"Tổng tiền nhập: {sum_nhap:,.0f} VND")
        self.lbl_sum_xuat.configure(text=f"Tổng tiền xuất: {sum_xuat:,.0f} VND")
        self.lbl_sum_gd.configure(text=f"Số lượng giao dịch: {count_gd}")
        
        # Clear Treeview
        for item in self.month_tree.get_children():
            self.month_tree.delete(item)
            
        for gd in filtered:
            loai_lbl = "Nhập kho" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "Xuất kho"
            tag = "nhap" if gd.loai_giao_dich == GiaoDich.LOAI_NHAP else "xuat"
            self.month_tree.insert("", "end", values=(
                gd.ma_gd,
                f"{gd.ten_sp} ({gd.ma_sp})",
                loai_lbl,
                gd.so_luong,
                f"{gd.don_gia:,.0f}",
                f"{gd.thanh_tien():,.0f}",
                gd.ngay_thuc_hien,
                gd.ghi_chu
            ), tags=(tag,))

    def generate_stock_stats(self):
        products = tai_danh_sach_san_pham()
        
        # 1. Left Table: Sorted descending
        sorted_products = _sap_xep_giam_dan_gia_tri(products)
        
        for item in self.stock_val_tree.get_children():
            self.stock_val_tree.delete(item)
            
        for sp in sorted_products:
            self.stock_val_tree.insert("", "end", values=(
                sp.ma_sp,
                sp.ten_sp,
                sp.loai_hang,
                sp.so_luong_ton,
                f"{sp.don_gia:,.0f}",
                f"{sp.thanh_tien():,.0f}"
            ))
            
        # 2. Right Table: Category breakdown
        stats = _thong_ke_theo_loai(products) # returns list of lists: [[loai, count, sum_val], ...]
        total_val = sum(sp.thanh_tien() for sp in products)
        
        for item in self.cat_stats_tree.get_children():
            self.cat_stats_tree.delete(item)
            
        for row in stats:
            loai_hang = row[0]
            sum_val = row[1]
            count = row[2]
            ratio_pct = (sum_val / total_val * 100) if total_val > 0 else 0
            
            self.cat_stats_tree.insert("", "end", values=(
                loai_hang,
                count,
                f"{sum_val:,.0f}",
                f"{ratio_pct:.1f}%"
            ))

def start_gui():
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
