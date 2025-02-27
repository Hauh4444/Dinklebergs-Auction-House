from ..database import get_db
from ..entities.review import Review

class ReviewMapper:
    """Handles database operations related to reviews."""

    @staticmethod
    def get_all_reviews(args):

        db = get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM reviews"
        values = []

        # Add conditions
        if "listing_id" in args:
            statement += " WHERE listing_id=?"
            values.append(args["listing_id"])

        # Add sorting
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"

        # Add start and range
        if "start" in args and "range" in args:
            statement += " LIMIT ? OFFSET ?"
            values.extend([args["range"], args["start"]])

        cursor.execute(statement, values)
        reviews = cursor.fetchall()
        return [Review(**review).to_dict() for review in reviews]

    @staticmethod
    def get_review_by_id(review_id):
        """Retrieve a review by its ID.

        Args:
            review_id (int): The ID of the review to retrieve.

        Returns:
            dict: Review details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reviews WHERE review_id=?", (review_id,))
        review = cursor.fetchone()
        return Review(**review).to_dict() if review else None

    @staticmethod
    def create_review(data):
        """Create a new review in the database.

        Args:
            data (dict): Dictionary containing review details.

        Returns:
            int: The ID of the newly created review.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO reviews 
            (listing_id, user_id, username, title, description, stars, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        # Explicitly extract the values from the data dictionary, excluding review_id if it exists
        values = [
            data['listing_id'],
            data['user_id'],
            data['username'],
            data['title'],
            data['description'],
            data['stars'],
            data['created_at']
        ]
        cursor.execute(statement, values)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_review(review_id, data):
        """Update an existing review.

        Args:
            review_id (int): The ID of the review to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        conditions = [f"{key}=?" for key in data if key != "review_id"]
        values = list(data.values())
        values.append(review_id)
        statement = "UPDATE reviews SET " + ", ".join(conditions) + " WHERE review_id=?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_review(review_id):
        """Delete a review by its ID.

        Args:
            review_id (int): The ID of the review to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM reviews WHERE review_id=?", (review_id,))
        db.commit()
        return cursor.rowcount
