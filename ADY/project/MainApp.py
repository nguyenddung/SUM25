import tkinter as tk
from DatabaseConnect import DatabaseConnection
from query_handler import QueryHandler
from gui_products import ProductGUI
from gui_orders import OrderGUI
from gui_employees import EmployeeGUI


class MainApp:
    def __init__(self, root):
        ### Quan oi ong thay doi ten sever o day !!!! ###
        self.db = DatabaseConnection(server="AUSTINNGUYEN", database="Northwind")
        self.query_handler = QueryHandler(self.db)

        root.title("🏠 Quản lý Hệ thống")
        root.geometry("400x200")

        tk.Button(root, text="Quản lý Sản phẩm", command=self.open_product_gui).pack(
            pady=10
        )
        tk.Button(root, text="Quản lý Đơn hàng", command=self.open_order_gui).pack(
            pady=10
        )
        tk.Button(root, text="Quản lý Nhân viên", command=self.open_employee_gui).pack(
            pady=10
        )

    def open_product_gui(self):
        ProductGUI(self.db, self.query_handler)

    def open_order_gui(self):
        OrderGUI(self.db, self.query_handler)

    def open_employee_gui(self):
        EmployeeGUI(self.db, self.query_handler)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
