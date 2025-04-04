from flask import jsonify, Response

import socketio

from ..data_mappers import BidMapper  # Assuming you have a BidMapper for DB interactions


class BidService:
    @staticmethod
    def post_bid(data, db_session=None):
        """
        Posts a new bid and broadcasts it in real-time.

        Args:
            data (dict): A dictionary containing the bid details (e.g., user, amount).
            db_session (Optional[Session]): An optional database session used for testing.

        Returns:
            Response: A JSON response containing the success message, bid ID, and bid data if successful.
                Returns status code 400 if required fields are missing.
        """
        # Validation to check if required fields are present
        if not data.get("user") or not data.get("amount"):
            data = {"error": "User and amount are required"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')

        # Save the bid using the BidMapper to interact with the DB
        bid_id = BidMapper.create_bid(data=data, db_session=db_session)

        socket = socketio.AsyncServer()

        # Broadcast the new bid in real-time to all connected clients
        socket.emit('new_bid', data)  # Emit event to all connected clients

        # Return the success message with the bid ID and data
        data = {"message": "Bid posted", "bid_id": bid_id, "bid": data}
        return Response(response=jsonify(data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def get_bid_by_id(bid_id, db_session=None):
        """
        Retrieves a specific bid by its ID.

        Args:
            bid_id (int): The ID of the bid to retrieve.
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the bid data if found.
                Returns status code 404 if the bid is not found.
        """
        # Use BidMapper to get the bid from the database by its ID
        bid = BidMapper.get_bid_by_id(bid_id=bid_id, db_session=db_session)

        if bid:
            # If found, return the bid data in a Response object
            data = {"message": "Bid found", "bid": bid}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        # If the bid is not found, return an error message
        data = {"error": "Bid not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_all_bids(db_session=None):
        """
        Retrieves a list of all bids.

        Args:
            db_session (Optional[Session]): An optional database session to be used in tests.

        Returns:
            Response: A JSON response containing the list of all bids.
        """
        # Use BidMapper to get all bids from the database
        bids = BidMapper.get_all_bids(db_session=db_session)

        # Return the list of bids in the response
        data = {"message": "Bids found", "bids": bids}
        return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
