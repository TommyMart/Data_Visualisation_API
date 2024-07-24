# Built-in Python Libraries

# External Libraries
from flask_jwt_extended import get_jwt_identity

# Imports from local files
from init import db
from models.user import User

# Define a function to check if the user is an admin


def authorise_as_admin():
    # get the users id from get_jwt_identity()
    user_id = get_jwt_identity()
    # fetch the user from the DB
    stmt = db.select(User).filter_by(id=user_id)
    # fetch the user from the DB with correct id
    user = db.session.scalar(stmt)
    # return True if the user is an admin
    return user.is_admin
