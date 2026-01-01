import tkinter as tk
from tkinter import messagebox


class ProductGUI(tk.Toplevel):
    def __init__(self, db, query_handler):
        super().__init__()
        self.db = db
        self.query_handler = query_handler
        self.title("📦 Quản lý Sản phẩm")
        self.geometry("400x350")

        tk.Label(self, text="ID:").grid(row=0, column=0)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=0, column=1)

        tk.Label(self, text="Tên SP:").grid(row=1, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self, text="Giá:").grid(row=2, column=0)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=2, column=1)

        tk.Button(self, text="Thêm SP", command=self.insert_product).grid(
            row=3, column=0
        )
        tk.Button(self, text="Xem danh sách", command=self.get_products).grid(
            row=3, column=1
        )
        # ...existing code...

        tk.Label(self, text="ID cần xem:").grid(row=6, column=0)
        self.filter_id_entry = tk.Entry(self)
        self.filter_id_entry.grid(row=6, column=1)

        tk.Button(
            self,
            text="Xem SP & NCC theo ID",
            command=self.show_product_with_supplier_by_id,
        ).grid(row=7, column=0, columnspan=2, pady=10)

    def insert_product(self):
        self.query_handler.insert_product(
            self.id_entry.get(),
            self.name_entry.get(),
            None,
            None,
            self.price_entry.get(),
        )
        messagebox.showinfo("Thông báo", "✅ Đã thêm sản phẩm!")

    def get_products(self):
        products = self.query_handler.get_all_products()
        messagebox.showinfo(
            "📜 Danh sách sản phẩm", "\n".join(str(p) for p in products)
        )

    def show_product_with_supplier_by_id(self):
        product_id = self.filter_id_entry.get()
        if not product_id.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng nhập ID là số!")
            return
        results = self.query_handler.get_products_with_suppliers(int(product_id))
        if not results:
            messagebox.showinfo("Kết quả", "Không có dữ liệu.")
            return
        lines = [f"ID: {r[0]}, Tên: {r[1]}, NCC: {r[2]}, Giá: {r[3]}" for r in results]
        messagebox.showinfo("Sản phẩm & Nhà cung cấp", "\n".join(lines))
