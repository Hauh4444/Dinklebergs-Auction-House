from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import ChatMapper


class ChatService:
    @staticmethod
    def get_chats(db_session=None):
        """
        Fetch all support chats for the authenticated user.

        Args:
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response containing the user's chats if available, otherwise a 404 error.
        """
        chats = ChatMapper.get_chats_by_user_id(user_id=current_user.id, db_session=db_session)
        if not chats:
            return Response(response=jsonify({"error": "No chats found"}).get_data(), status=404, mimetype='application/json')

        return Response(response=jsonify({"message": "Chats retrieved", "chats": chats}).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def get_chat_by_id(chat_id, db_session=None):
        """
        Retrieve details of a specific support chat by ID.

        Args:
            chat_id (int): Unique identifier of the chat.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response with chat details if found, otherwise a 404 error.
        """
        chat = ChatMapper.get_chat_by_id(chat_id=chat_id, db_session=db_session)
        if not chat:
            return Response(response=jsonify({"error": "Chat not found"}).get_data(), status=404, mimetype='application/json')

        return Response(response=jsonify({"message": "Chat retrieved", "chat": chat}).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def create_chat(data, db_session=None):
        """
        Create a new support chat.

        Args:
            data (dict): Payload containing details for creating the chat.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response with the created chat ID if successful, otherwise a 409 error.
        """
        chat_id = ChatMapper.create_chat(data=data, db_session=db_session)
        if not chat_id:
            return Response(response=jsonify({"error": "Error creating Chat"}).get_data(), status=409, mimetype='application/json')

        return Response(response=jsonify({"message": "Chat and message created", "chat_id": chat_id}).get_data(), status=201, mimetype='application/json')


    @staticmethod
    def update_chat(chat_id, data, db_session=None):
        """
        Update an existing support chat.

        Args:
            chat_id (int): Unique identifier of the chat to update.
            data (dict): Payload containing updated chat details.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response confirming update success or a 404 error if the chat is not found.
        """
        updated_rows = ChatMapper.update_chat(chat_id=chat_id, data=data, db_session=db_session)
        if not updated_rows:
            return Response(response=jsonify({"error": "Error updating chat"}).get_data(), status=409, mimetype="application/json")

        return Response(response=jsonify({"message": "Chat updated", "updated_rows": updated_rows}).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_chat(chat_id, db_session=None):
        """
        Delete a support chat by ID.

        Args:
            chat_id (int): Unique identifier of the chat to delete.
            db_session (Session, optional): Database session for executing queries.

        Returns:
            Response: JSON response confirming deletion success or a 404 error if the chat is not found.
        """
        deleted_rows = ChatMapper.delete_chat(chat_id=chat_id, db_session=db_session)
        if not deleted_rows:
            return Response(response=jsonify({"error": "Chat not found"}).get_data(), status=404, mimetype="application/json")

        return Response(response=jsonify({"message": "Chat deleted", "deleted_rows": deleted_rows}).get_data(), status=200, mimetype="application/json")