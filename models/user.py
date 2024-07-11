# "user" table model and schema

from init import db, ma
from marshmallow import fields

# create model class extended from the sqlalchemy model class 
class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table 
    # id column - integer data value and primary key of "users" table
    id = db.Column(db.Integer, primary_key=True)
    # name column - string data value 
    name = db.Column(db.String)
    user_name = db.Column(db.String)
    # password column - string data value and cannot be null
    password = db.Column(db.String, nullable=False)
    # email column - string data value, cannot be null and must be unique
    email = db.Column(db.String, nullable=False, unique=True)
    dob = db.Column(db.Date)
    # is_admin column - boolean value and cannot be null
    is_admin = db.Column(db.Boolean, default=False)

    # connects the two variables user and post from posts.py
    # connects to the Post model and user field, provided by sqlalchemy
    # a user can have 0 or multple posts
    posts = db.relationship("Post", back_populates="user")


# schema instance from marshmallow - convert db objects to python objects
# and python objects to db objects
class UserSchema(ma.Schema):

    # a user can have zero or more posts so it is a list, each object in 
    # the field is a nested object. Use PostSchema to serialise and deserialise,
    posts = fields.List(fields.Nested("PostSchema", exclude=["user"]))


    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "posts")


# user_schema object set to call UserSchema class
# we do not want to pass the password back to the user so we exclude it
# to handle a single user object
# must exclude user so it does not make a never ending loop
user_schema = UserSchema(exclude=["password"])
# to handle a list user objects
users_schema = UserSchema(many=True, exclude=["password"])