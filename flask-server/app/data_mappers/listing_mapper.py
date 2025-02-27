from ..database import get_db
from ..entities.listing import Listing


class ListingMapper:
    """Handles database operations related to listings."""

    @staticmethod
    def get_all_listings(args):
        """Retrieve all listings with optional filtering, sorting, and pagination.

        Args:
            args (dict): Dictionary of query parameters (e.g., category_id, min_price, query).

        Returns:
            list: A list of listing dictionaries matching the query conditions.
        """
        db = get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM listings"
        conditions = []
        values = []

        # Add conditions
        if "category_id" in args:
            conditions.append("category_id=?")
            values.append(args["category_id"])
        if "listing_type" in args:
            conditions.append("listing_type=?")
            values.append(args["listing_type"])
        if "min_price" in args:
            conditions.append("buy_now_price > ?")
            values.append(args["min_price"])
        if "max_price" in args:
            conditions.append("buy_now_price < ?")
            values.append(args["max_price"])
        if "query" in args:
            query = args["query"]
            conditions.append("(title LIKE ? OR description LIKE ?)")
            values.extend([f'%{query}%', f'%{query}%'])

        if conditions:
            statement += " WHERE " + " AND ".join(conditions)

        # Add sorting
        if "sort" in args and "order" in args:
            statement += f" ORDER BY {args['sort']} {args['order'].upper()}"

        # Add pagination
        if "start" in args and "range" in args:
            statement += " LIMIT ? OFFSET ?"
            values.extend([args["range"], args["start"]])

        cursor.execute(statement, values)
        listings = cursor.fetchall()
        return [Listing(**listing).to_dict() for listing in listings]

    @staticmethod
    def get_listing_by_id(listing_id):
        """Retrieve a single listing by its ID.

        Args:
            listing_id (int): The ID of the listing to retrieve.

        Returns:
            dict: Listing details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM listings WHERE listing_id=?", (listing_id,))
        listing = cursor.fetchone()
        return Listing(**listing).to_dict() if listing else None

    @staticmethod
    def create_listing(data):
        """Create a new listing in the database.

        Args:
            data (dict): Dictionary containing listing details.

        Returns:
            int: The ID of the newly created listing.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO listings 
            (listing_id, user_id, title, title_short, description, item_specifics, category_id, listing_type, starting_price, 
            reserve_price, current_price, buy_now_price, auction_start, auction_end, status, image_encoded, bids, purchases, 
            average_review, total_reviews, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Listing(**data).to_dict().values()))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_listing(listing_id, data):
        """Update an existing listing.

        Args:
            listing_id (int): The ID of the listing to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        set_clause = ", ".join([f"{key}=?" for key in data if key not in ["listing_id", "created_at"]])
        values = [data[key] for key in data if key not in ["listing_id", "created_at"]]
        values.append(listing_id)
        statement = f"UPDATE listings SET {set_clause} WHERE listing_id=?"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_listing(listing_id):
        """Delete a listing by its ID.

        Args:
            listing_id (int): The ID of the listing to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM listings WHERE listing_id=?", (listing_id,))
        db.commit()
        return cursor.rowcount

