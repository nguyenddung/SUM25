import tkinter as tk
from tkinter import messagebox


class OrderGUI(tk.Toplevel):
    def __init__(self, db, query_handler):
        super().__init__()
        self.db = db
        self.query_handler = query_handler
        self.title("📦 Quản lý Đơn hàng")
        self.geometry("400x350")

        tk.Label(self, text="ID Đơn hàng:").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(self)
        self.order_id_entry.grid(row=0, column=1)

        tk.Button(self, text="Xem đơn hàng", command=self.get_orders).grid(
            row=1, column=0, columnspan=2, padx=10, pady=10
        )

        tk.Label(self, text="Xem chi tiết ĐH ID:").grid(row=4, column=0)
        self.detail_order_id_entry = tk.Entry(self)
        self.detail_order_id_entry.grid(row=4, column=1)

        tk.Button(
            self,
            text="Xem chi tiết đơn hàng",
            command=self.show_order_detail_by_id,
        ).grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def get_orders(self):
        orders = self.query_handler.get_all_orders()
        if not orders:
            messagebox.showinfo("📜 Danh sách đơn hàng", "Không có đơn hàng nào.")
            return
        lines = []
        for o in orders:
            # Giả sử cột 0: OrderID, 1: CustomerID, 2: EmployeeID, 3: OrderDate
            lines.append(
                f"OrderID: {o[0]}, Customer: {o[1]}, Employee: {o[2]}, Date: {o[3]}"
            )
        messagebox.showinfo("📜 Danh sách đơn hàng", "\n".join(lines))

    def show_order_detail_by_id(self):
        order_id = self.detail_order_id_entry.get()
        if not order_id.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng nhập OrderID là số!")
            return
        orders = self.query_handler.get_orders_with_customer_employee_by_id(
            int(order_id)
        )
        if not orders:
            messagebox.showinfo("Kết quả", "Không có dữ liệu.")
            return
        lines = [
            f"OrderID: {o[0]}, Khách: {o[1]}, Nhân viên: {o[2]}, Ngày: {o[3]}"
            for o in orders
        ]
        messagebox.showinfo("Chi tiết đơn hàng", "\n".join(lines))
