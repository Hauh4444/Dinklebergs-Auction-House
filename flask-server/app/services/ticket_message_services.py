from flask import jsonify, Response

from ..data_mappers import TicketMessageMapper, SupportTicketMapper
from ..utils.socketio import socketio


class TicketMessageService:
    @staticmethod
    def get_messages_by_ticket_id(ticket_id, db_session=None):
        """
        Retrieve all messages for a given support ticket.

        Args:
            ticket_id (int): The ID of the ticket for which messages are to be retrieved.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the ticket messages if found, otherwise a 404 error.
        """
        messages = TicketMessageMapper.get_messages_by_ticket_id(ticket_id=ticket_id, db_session=db_session)
        if not messages:
            response_data = {"error": "No messages found for this ticket"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Messages found", "ticket_messages": messages}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new message for a support ticket.

        Args:
            data (dict): A dictionary containing the message data (e.g., ticket_id, message content).
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with the success message and message ID, or a 409 error if the message could not be created.
        """
        message_id = TicketMessageMapper.create_message(data=data, db_session=db_session)
        if not message_id:
            response_data = {"error": "Error creating message"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        updated_rows = SupportTicketMapper.update_ticket_timestamp(ticket_id=data.get("ticket_id"), db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating ticket timestamp"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        socketio.emit('new_ticket_message', {"message_id": message_id})

        response_data = {"message": "Message created", "message_id": message_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_message(message_id, updates, db_session=None):
        """
        Update an existing ticket message.

        Args:
            message_id (int): The ID of the message to be updated.
            updates (dict): A dictionary containing the updates to be applied to the message.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with a success message if the message was updated, or a 404 error if the message was not found or no changes were made.
        """
        updated_rows = TicketMessageMapper.update_message(message_id=message_id, updates=updates, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating ticket message"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype='application/json')

        response_data = {"message": "Ticket message updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def delete_message(message_id, db_session=None):
        """
        Delete a ticket message by its ID.

        Args:
            message_id (int): The ID of the message to be deleted.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with the success message if the message was deleted, or a 404 error if the message was not found.
        """
        deleted_rows = TicketMessageMapper.delete_message(message_id=message_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Message not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Message deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')
