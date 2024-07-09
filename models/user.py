# "user" table model and schema

from init import db, ma

# create model class extended from the sqlalchemy model class 
class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table 
    # id column - integer data value and primary key of "users" table
    id = db.Column(db.Integer, primary_key=True)
    # name column - string data value 
    name = db.Column(db.String)
    # email column - string data value, cannot be null and must be unique
    email = db.Column(db.String, nullable=False, unique=True)
    # password column - string data value and cannot be null
    password = db.Column(db.String, nullable=False)
    # is_admin column - boolean value and cannot be null
    is_admin = db.Column(db.Boolean, default=False)

# schema instance from marshmallow - convert db objects to python objects
# and python objects to db objects
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin")


# user_schema object set to call UserSchema class
# we do not want to pass the password back to the user so we exclude it
# to handle a single user object
user_schema = UserSchema(exclude=["password"])
# # to handle a list user objects
users_schema = UserSchema(many=True, exclude=["password"])