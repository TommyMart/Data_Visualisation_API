# Built-in Python Libraries
from datetime import timedelta

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

# Imports from local files
from init import bcrypt, db
from models.user import User, user_schema, users_schema, UserSchema
from utils import authorise_as_admin

# Create a Blueprint for user-related routes
user_bp = Blueprint("user", __name__, url_prefix="/user")

# Route to fetch all users
# /user/


@user_bp.route("/", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def get_users():
    try:
        """
        Fetch all users from the database.
        """
        stmt = db.select(User).order_by(
            User.id.asc())  # Prepare SQL query to fetch all users
        users = db.session.scalars(stmt)  # Execute the query
        # Return the users with status code 200
        return users_schema.dump(users), 200
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to fetch a single user by user_id
# /user/<int:user_id>


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def get_user(user_id):
    try:
        """
        Fetch a single user by user_id from the database.
        """
        stmt = db.select(User).filter_by(
            id=user_id)  # Prepare SQL query to fetch user by ID
        user = db.session.scalar(stmt)  # Execute the query
        if user:
            # Return the user with status code 200
            return user_schema.dump(user), 200
        else:
            # Return error if user not found
            return {"error": f"User with id {user_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to search users by partial user_name
# /user/search/<string:user_name>


@user_bp.route("/search/<string:user_name>", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def search_user_by_name(user_name):
    try:
        """
        Search for users by partial user_name.
        """
        like_pattern = f"%{
            user_name}%"  # Construct LIKE pattern for partial matching
        # Prepare SQL query with case-insensitive LIKE
        stmt = db.select(User).filter(User.user_name.ilike(like_pattern))
        # Execute the query and fetch all matching users
        users = db.session.scalars(stmt).all()
        if users:
            # Return the users with status code 200
            return users_schema.dump(users), 200
        else:
            # Return error if no users found
            return {"error": f"No users found matching '{user_name}'"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to update a user
# /user/<int:user_id>


@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect the route with JWT authentication
def update_user(user_id):
    try:
        """
        Update a user's details.
        """
        body_data = UserSchema().load(
            request.get_json(), partial=True)  # Load and validate request data
        # Get the password from the request data
        password = body_data.get("password")
        # Prepare SQL query to fetch user by ID
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)  # Execute the query
        if user:
            # Ensure the user is authorized to make the update
            if str(user.id) != get_jwt_identity():
                # Return forbidden error if unauthorized
                return {"error": "Only the creator of a post can update it"}, 403
            # Update user fields if present
            user.name = body_data.get("name") or user.name
            user.user_name = body_data.get("user_name") or user.user_name
            if password:
                user.password = bcrypt.generate_password_hash(
                    password).decode("utf-8")  # Hash and update password
            db.session.commit()  # Commit changes to the database
            # Return updated user with status code 200
            return user_schema.dump(user), 200
        else:
            # Return error if user does not exist
            return {"error": "User does not exist"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to delete a user
# /user/<int:user_id>


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()  # Protect the route with JWT authentication
def delete_user(user_id):
    try:
        """
        Delete a user from the database.
        """
        stmt = db.select(User).filter_by(
            id=user_id)  # Prepare SQL query to fetch user by ID
        user = db.session.scalar(stmt)  # Execute the query
        if user:
            is_admin = authorise_as_admin()  # Check if the current user is an admin
            # Ensure the user is authorized to delete the user
            if not is_admin and str(user.id) != get_jwt_identity():
                # Return forbidden error if unauthorized
                return {"error": "User unauthorized to perform this request"}, 403
            db.session.delete(user)  # Delete the user
            db.session.commit()  # Commit changes to the database
            # Return success message with status code 200
            return {"message": f"User '{user.name}' deleted successfully"}, 200
        else:
            # Return error if user not found
            return {"error": f"User with id '{user_id}' not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500
