
from datetime import timedelta

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

from init import bcrypt, db
from models.user import User, user_schema, UserSchema


user_bp = Blueprint("user", __name__, url_prefix="/user")

# user/<int:user_id>
@user_bp.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    # get the fields from the body of request
    body_data = UserSchema().load(request.get_json(), partial=True)
    password = body_data.get("password")
    # fetch user from the DB
    stmt = db.select(User).filter_by(id=get_jwt_identity())
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
