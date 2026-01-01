class QueryHandler:
    def __init__(self, db):
        self.db = db

    # PRODUCTS
    def get_all_products(self):
        query = "SELECT * FROM Products"
        return self.db.fetch_all(query)

    def insert_product(self, product_id, name, supplier_id, category_id, price):
        query = "INSERT INTO Products (ProductID, ProductName, SupplierID, CategoryID, UnitPrice) VALUES (?, ?, ?, ?, ?)"
        self.db.execute_query(
            query, (product_id, name, supplier_id, category_id, price)
        )
        print("🆕 Sản phẩm đã được thêm!")

    def update_product(self, product_id, price):
        query = "UPDATE Products SET UnitPrice = ? WHERE ProductID = ?"
        self.db.execute_query(query, (price, product_id))
        print("📝 Giá sản phẩm đã được cập nhật!")

    def delete_product(self, product_id):
        query = "DELETE FROM Products WHERE ProductID = ?"
        self.db.execute_query(query, (product_id,))
        print("🗑️ Sản phẩm đã bị xóa!")

    # EMPLOYEES

    def get_all_employees(self):
        query = "SELECT TOP 50 * FROM Employees"
        return self.db.fetch_all(query)

    def insert_employee(self, last_name, first_name, title):
        query = """
            INSERT INTO Employees (LastName, FirstName, Title)
            VALUES (?, ?, ?)
        """
        self.db.execute_query(query, (last_name, first_name, title))
        print("🆕 Nhân viên đã được thêm!")

    def update_employee(self, emp_id, title):
        query = "UPDATE Employees SET Title = ? WHERE EmployeeID = ?"
        self.db.execute_query(query, (title, emp_id))
        print("📝 Chức vụ nhân viên đã được cập nhật!")

    def delete_employee(self, emp_id):
        query = "DELETE FROM Employees WHERE EmployeeID = ?"
        self.db.execute_query(query, (emp_id,))
        print("🗑️ Nhân viên đã bị xóa!")

    # ORDERS
    def get_all_orders(self):
        query = "SELECT TOP 50 * FROM Orders"
        return self.db.fetch_all(query)

    def insert_order(self, order_id, customer_id, employee_id, order_date):
        query = "INSERT INTO Orders (OrderID, CustomerID, EmployeeID, OrderDate) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (order_id, customer_id, employee_id, order_date))
        print("🆕 Đơn hàng đã được thêm!")

    def update_order(self, order_id, order_date):
        query = "UPDATE Orders SET OrderDate = ? WHERE OrderID = ?"
        self.db.execute_query(query, (order_date, order_id))
        print("📝 Ngày đặt hàng đã được cập nhật!")

    def delete_order(self, order_id):
        query = "DELETE FROM Orders WHERE OrderID = ?"
        self.db.execute_query(query, (order_id,))
        print("🗑️ Đơn hàng đã bị xóa!")

    ### cac cau lenh join tren sql

    # JOIN PRODUCTS VỚI SUPPLIERS
    def get_products_with_suppliers(self, product_id=None):
        query = """
                SELECT p.ProductID, p.ProductName, s.CompanyName AS SupplierName, p.UnitPrice
                FROM Products p
                JOIN Suppliers s ON p.SupplierID = s.SupplierID
            """
        params = ()
        if product_id:
            query += " WHERE p.ProductID = ?"
            params = (product_id,)
        query += " ORDER BY p.ProductID"
        return self.db.fetch_all(query, params)

    def get_orders_with_customer_employee_by_id(self, order_id):
        query = """
            SELECT o.OrderID, c.CompanyName AS CustomerName, e.FirstName + ' ' + e.LastName AS EmployeeName, o.OrderDate
            FROM Orders o
            JOIN Customers c ON o.CustomerID = c.CustomerID
            JOIN Employees e ON o.EmployeeID = e.EmployeeID
            WHERE o.OrderID = ?
        """
        return self.db.fetch_all(query, (order_id,))
