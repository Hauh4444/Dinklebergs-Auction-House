from ..database import get_db
from ..entities.order import Order

class OrderMapper:
    """Handles database operations related to orders."""

    @staticmethod
    def get_all_orders():
        """Retrieve all orders from the database.

        Returns:
            list: A list of order dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return [Order(**order).to_dict() for order in orders]

    @staticmethod
    def get_order_by_id(order_id):
        """Retrieve an order by its ID.

        Args:
            order_id (int): The ID of the order to retrieve.

        Returns:
            dict: Order details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        return Order(**order).to_dict() if order else None

    @staticmethod
    def create_order(data):
        """Create a new order in the database.

        Args:
            data (dict): Dictionary containing order details.

        Returns:
            int: The ID of the newly created order.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO orders 
            (user_id, order_date, status, total_amount, payment_status, payment_method, 
            shipping_address, shipping_method, tracking_number, shipping_cost, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Order(**data).to_dict().values())[1:])  # Exclude order_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_order(order_id, data):
        """Update an existing order.

        Args:
            order_id (int): The ID of the order to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data if key not in ["order_id", "created_at"]]
        values = [data[key] for key in data if key not in ["order_id", "created_at"]]
        values.append(order_id)
        statement = f"UPDATE orders SET {', '.join(conditions)}, updated_at = CURRENT_TIMESTAMP WHERE order_id = ?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_order(order_id):
        """Delete an order by its ID.

        Args:
            order_id (int): The ID of the order to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()

