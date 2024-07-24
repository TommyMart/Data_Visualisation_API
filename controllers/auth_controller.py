# Built-in Python Libraries
from datetime import timedelta

# External Libraries
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token

# Imports from local files
from init import bcrypt, db
from models.user import User, user_schema, UserSchema

# Define the blueprint named "auth"
# Routes have the same "auth" prefix, so we can include a url_prefix 
# to cover all routes within the "auth" blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Create the auth/register route
# POST method because a user is adding data to the database
# Route: http://localhost:8080/auth/register, Methods: POST
@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user by adding their data to the database.
    """
    try:
        # Get the payload/data from the body of the request
        body_data = UserSchema().load(request.get_json())

        # Create an instance of the User model to register new data
        user = User(
            name=body_data.get("name"),
            user_name=body_data.get("user_name"),
            email=body_data.get("email"),
            dob=body_data.get("dob"),
            is_admin=body_data.get("is_admin")
        )

        # Extract the password from the body/payload
        password = body_data.get("password")

        # Hash the password if the user entered a password
        if password:
            # Add the hashed password to the user instance
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Add and commit the new user instance to the database
        db.session.add(user)
        db.session.commit()

        # Respond back to the user/frontend with the new user's data
        return user_schema.dump(user), 201

    # Handle database integrity errors
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # Handle not null violation error
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # Handle unique violation error
            return {"error": "Email address already in use"}, 409

# Route: http://localhost:8080/auth/login, Methods: POST
# POST method because data is being sent in the request from the client
@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Log in a user by verifying their email and password, and return a JWT token.
    """
    # Get the data from the body of the request
    body_data = request.get_json()

    # Find the user in the database with the provided email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)

    # Check if user exists and if the password matches the email
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # Create a JWT token
        # Identity is the id of the user, which must be converted to a string
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

        # Respond back to the frontend with the user's email, admin status, and token
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    else:
        # If user doesn't exist or password doesn't match, respond with an error
        return {"error": "Invalid email or password"}, 401