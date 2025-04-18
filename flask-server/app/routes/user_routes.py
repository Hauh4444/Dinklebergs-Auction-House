from flask import Blueprint, request
from flask_login import login_required, current_user

from ..services import UserService

# Blueprint for user login-related routes
bp = Blueprint("user_bp", __name__, url_prefix="/api/user")


# GET /api/user/
@bp.route("/", methods=["GET"])
@login_required
def get_user(db_session=None):
    """
    Get the details of the currently logged-in user.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response with user details.
    """
    data = None
    if current_user.role in ["staff", "admin"]:
        data = request.args.to_dict()

    return UserService.get_user(data=data, db_session=db_session)


# PUT /api/user/{id}/
@bp.route("/<int:user_id>/", methods=["PUT"])
@login_required
def update_user(user_id, db_session=None):
    """
    Updates a user.

    Args:
        user_id (int): The id of the user to update
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated profile details.

    Returns:
        JSON response indicating the updated profile.
    """
    data = request.json
    return UserService.update_user(user_id=user_id, data=data, db_session=db_session)


# DELETE /api/user/{id}/
@bp.route("/<int:user_id>/", methods=["DELETE"])
@login_required
def delete_user(user_id, db_session=None):
    """
    Delete the user login credentials and profile.

    Args:
        user_id (int): The id of the user to delete
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    return UserService.delete_user(user_id=user_id, db_session=db_session)