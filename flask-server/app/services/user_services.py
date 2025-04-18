from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import UserMapper, ProfileMapper


class UserService:
    @staticmethod
    def get_user(data=None, db_session=None):
        """
        Retrieves a user by their ID.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the user details if found, otherwise a 404 error with a message.
        """
        if current_user.role in ["staff", "admin"]:
            user = UserMapper.get_user(user_id=data.get("user_id"), db_session=db_session)
        else:
            user = UserMapper.get_user(user_id=current_user.id, db_session=db_session)

        if not user:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User found", "user": user}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def update_user(user_id, data=None, db_session=None):
        """
        Updates user information.

        Args:
            user_id (int): The id of the user to update
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success or an error message if the user is not found.
        """
        del data["created_at"], data["last_login"]
        if current_user.role in ["staff", "admin"]:
            updated_rows = UserMapper.update_user(user_id=user_id, data=data, db_session=db_session)
        else:
            updated_rows = UserMapper.update_user(user_id=current_user.id, data=data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "Error updating user"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "User updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_user(user_id, db_session=None):
        """
        Deletes a user by their ID.

        Args:
            user_id (int): The id of the user to delete
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the user was deleted, or a 404 error if the user was not found.
        """
        if current_user.role in ["staff", "admin"]:
            deleted_rows = ProfileMapper.delete_profile(user_id=user_id, db_session=db_session)
        else:
            deleted_rows = ProfileMapper.delete_profile(user_id=current_user.id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        if current_user.role in ["staff", "admin"]:
            deleted_rows = UserMapper.delete_user(user_id=user_id, db_session=db_session)
        else:
            deleted_rows = UserMapper.delete_user(user_id=current_user.id, db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User and Profile deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")