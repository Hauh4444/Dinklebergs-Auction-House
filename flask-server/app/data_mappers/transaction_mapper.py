from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import Transaction


class TransactionMapper:
    @staticmethod
    def get_all_transactions(user_id: int, db_session=None):
        """
        Retrieve all transactions from the database.

        Args:
            user_id: ID of the user to retrieve transactions of
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of transaction dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        transactions = cursor.fetchall()
        return [Transaction(**transaction).to_dict() for transaction in transactions]


    @staticmethod
    def get_transaction_by_id(transaction_id: int, db_session=None):
        """
        Retrieve a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Transaction details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
        transaction = cursor.fetchone()
        return Transaction(**transaction).to_dict() if transaction else None

    @staticmethod
    def create_transaction(data: dict, db_session=None):
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)  # type: ignore

        # Avoid duplicates
        check_stmt = """
            SELECT transaction_id FROM transactions WHERE payment_intent_id = %s
        """
        cursor.execute(check_stmt, (data["payment_intent_id"],))
        existing = cursor.fetchone()
        if existing:
            return existing["transaction_id"]

        insert_stmt = """
            INSERT INTO transactions 
            (user_id, payment_intent_id, created_at, updated_at) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_stmt, tuple(Transaction(**data).to_dict().values())[1:])  # Exclude transaction_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_transaction(transaction_id: int, data: dict, db_session=None):
        """
        Update an existing transaction.

        Args:
            transaction_id (int): The ID of the transaction to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    pass
            if isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        conditions = [f"{key} = %s" for key in data if key not in ["transaction_id", "created_at", "updated_at"]]
        values = [data.get(key) for key in data if key not in ["transaction_id", "created_at", "updated_at"]]
        values.append(datetime.now())
        values.append(transaction_id)
        statement = f"UPDATE transactions SET {', '.join(conditions)}, updated_at = %s WHERE transaction_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_transaction(transaction_id: int, db_session=None):
        """
        Delete a transaction by its ID.

        Args:
            transaction_id (int): The ID of the transaction to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
        db.commit()
        return cursor.rowcount
