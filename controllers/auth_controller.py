# Authorisation controller
# seperate file follows seperation of concerns (SoC)

from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db
from models.user import User, user_schema

# - define the blueprint named "auth" 
# - routes have same "auth" prefix so we can include a url_prefix 
# to cover all routes within the "auth" blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# create the auth/register route
# POST method because a user is adding data to the database
# route= http://localhost:8080/auth/register methods=POST
@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        # get the payload/data from the body of the request
        body_data = request.get_json()
        # create an instance of the user model to register new data
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
        )
        # extract the password from the body/payload
        password = body_data.get("password")

        # hash the password 
        # if the user entered a password
        if password:
            # user is the instance we created early in this function,
            # we are adding another attribute "password" to that that instance
            # of the User model
            # we have already extracted the password from the payload and assigned 
            # it to "password" that we use here
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit the new user instance to DB
        db.session.add(user)
        db.session.commit()

        # respond back to the user/frontend 
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not null violation
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 403
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation
            return {"error": "Email address already in use"}, 409



# route= http://localhost:8080/auth/login methods=GET
