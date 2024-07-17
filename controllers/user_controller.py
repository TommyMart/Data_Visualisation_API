# Built-in Python Libraries
from datetime import timedelta

# External Libraries
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

# Imports from local files
from init import bcrypt, db
from models.user import User, user_schema, users_schema, UserSchema
from utils import authorise_as_admin

# url_prefix = "/user" so routes do not need to include it
user_bp = Blueprint("user", __name__, url_prefix="/user")

# user/ - GET - fetch all users
@user_bp.route("/")
@jwt_required()
def get_users():
    stmt = db.select(User).order_by(User.id.asc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)

# user/<int:user_id> - GET - fetch single user
@user_bp.route("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    post = db.session.scalar(stmt)
    if post:
        return user_schema.dump(post)
    else:
        return {"error": f"Post with id {user_id} not found"}, 404

# user/<int:user_id> - PUT or PATCH - update user
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    # get the fields from the body of request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # fetch user from the DB
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # if user exists
    if user:
        # update the fields
        user.name = body_data.get("name") or user.name
        user.user_name = body_data.get("user_name") or user.user_name
        # if password included in body data
        if password:
            # hash new password using bcrypt
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # commit to DB
        db.session.commit()
        # return a response
        return user_schema.dump(user), 200
    # else
    else:
        # return an error
        return {"error": "User does not exist"}, 404

# user/<int:user_id> - DELETE - delete user
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # only admins can delete users
    is_admin = authorise_as_admin()
    if not is_admin:
        # if not admin return error and forbidden status
        return {"error": f"User is not authorised to perform this action"}, 403
    # fetch user from DB
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User '{user.name}' deleted successfully"}, 200
    
    else:
        return {"error": "User with id '{user_id}' not found"}