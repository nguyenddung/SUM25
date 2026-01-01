import tkinter as tk
from tkinter import messagebox


class EmployeeGUI(tk.Toplevel):
    def __init__(self, db, query_handler):
        super().__init__()
        self.db = db
        self.query_handler = query_handler
        self.title("👨‍💼 Quản lý Nhân viên")
        self.geometry("400x350")

        tk.Label(self, text="ID Nhân viên:").grid(row=0, column=0)
        self.employee_id_entry = tk.Entry(self)
        self.employee_id_entry.grid(row=0, column=1)

        tk.Label(self, text="Họ:").grid(row=1, column=0)
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self, text="Tên:").grid(row=2, column=0)
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=2, column=1)

        tk.Label(self, text="Chức vụ:").grid(row=3, column=0)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=3, column=1)

        tk.Button(self, text="Xem danh sách", command=self.get_employees).grid(
            row=4, column=0
        )
        tk.Button(self, text="Thêm nhân viên", command=self.insert_employee).grid(
            row=4, column=1
        )
        tk.Button(self, text="Cập nhật chức vụ", command=self.update_employee).grid(
            row=5, column=0
        )
        tk.Button(self, text="Xóa nhân viên", command=self.delete_employee).grid(
            row=5, column=1
        )

    def get_employees(self):
        employees = self.query_handler.get_all_employees()
        if not employees:
            messagebox.showinfo("📜 Danh sách nhân viên", "Không có nhân viên nào.")
            return
        lines = []
        for e in employees:
            # Giả sử cột 0: ID, 1: LastName, 2: FirstName, 3: Title
            lines.append(f"ID: {e[0]}, Họ: {e[1]}, Tên: {e[2]}, Chức vụ: {e[3]}")
        messagebox.showinfo("📜 Danh sách nhân viên", "\n".join(lines))

    def insert_employee(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        title = self.title_entry.get()
        self.query_handler.insert_employee(last_name, first_name, title)
        messagebox.showinfo("Thông báo", "✅ Đã thêm nhân viên!")

    def update_employee(self):
        emp_id = self.employee_id_entry.get()
        title = self.title_entry.get()
        self.query_handler.update_employee(emp_id, title)
        messagebox.showinfo("Thông báo", "📝 Đã cập nhật chức vụ!")

    def delete_employee(self):
        emp_id = self.employee_id_entry.get()
        self.query_handler.delete_employee(emp_id)
        messagebox.showinfo("Thông báo", "🗑️ Đã xóa nhân viên!")
