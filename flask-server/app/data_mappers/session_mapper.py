from pymysql import cursors

from ..database import get_db
from ..entities import Session
from datetime import datetime


class SessionMapper:
    @staticmethod
    def get_all_sessions(db_session=None):
        """
        Retrieve all sessions from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of session dictionaries retrieved from the database.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM sessions")
        sessions = cursor.fetchall()
        return [Session(**session).to_dict() for session in sessions]


    @staticmethod
    def get_session_by_id(session_id: int, db_session=None):
        """
        Retrieve a session by its ID from the database.

        Args:
            session_id (int): The ID of the session to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: A dictionary representation of the session if found, else None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM sessions WHERE session_id = %s", (session_id,))
        session = cursor.fetchone()
        return Session(**session).to_dict() if session else None


    @staticmethod
    def create_session(data: dict, db_session=None):
        """
        Create a new session in the database.

        Args:
            data (dict): The session data to be inserted into the database.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created session.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO sessions 
            (user_id, role, token, created_at, expires_at) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(Session(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_session(session_id: int, data: dict, db_session=None):
        """
        Update an existing session in the database.

        Args:
            session_id (int): The ID of the session to update.
            data (dict): The new data to update the session with.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The number of rows affected by the update.
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
        statement = """
            UPDATE sessions 
            SET user_id = %s, token = %s, role = %s, created_at = %s, expires_at = %s
            WHERE session_id = %s
        """
        cursor.execute(statement, tuple(Session(**data).to_dict().values())[1:] + (session_id,))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_session(session_id: int, db_session=None):
        """
        Delete a session by its ID.

        Args:
            session_id (int): The ID of the session to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM sessions WHERE session_id = %s", (session_id,))
        db.commit()
        return cursor.rowcount
