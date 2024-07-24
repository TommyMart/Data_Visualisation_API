

# External Libraries
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma
from models.like import Like

# TABLE
# create model class extended from the sqlalchemy model class 
class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table 
    # id column - integer data value and primary key of "users" table
    id = db.Column(db.Integer, primary_key=True)
    # name column - string data value 
    name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
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
    posts = db.relationship("Post", back_populates="user", cascade="all, delete")
    # Link with the comments field from the Comment model
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete")
    # Link with the likes field from the Comment model
    likes = db.relationship("Like", back_populates="user", cascade="all, delete")
    events = db.relationship("Event", back_populates="user", cascade="all, delete")
    attending = db.relationship("Attending", back_populates="user", cascade="all, delete")

# schema instance from marshmallow - convert db objects to python objects
# and python objects to db objects
class UserSchema(ma.Schema):

    # a user can have zero or more posts so it is a list, each object in 
    # the field is a nested object. Use PostSchema to serialise and deserialise,
    posts = fields.List(fields.Nested("PostSchema", exclude=["user"]))
    # A single user can make multiple comments (list)
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))
    # A single user can make multiple likes (list)
    likes = fields.List(fields.Nested("LikeSchema", exclude=["user"]))
    events = fields.List(fields.Nested("EventSchema", exclude=["user"]))
    attending = fields.List(fields.Nested("AttendingSchema", exclude=["user"]))

    # VALIDATION
    # name column - string data value and cannot be null
    name = fields.String(required=True, validate=And(
        # name must be between 3 and 50 characters long
        Length(min=3, max=50, error="Title must be 3 and 50 characters long"),
        # name must contain alphanumeric characters only
        Regexp(r"^[A-Za-z0-9 ]+$", error="Title must contain alphanumeric characters only")
        ))
    # user_name column - string data value and cannot be null
    user_name = fields.String(required=True, validate=And(
        # user name must be between 3 and 50 characters long
        Length(min=3, max=50, error="User name must be 3 and 50 characters long"),
        # user name must contain alphanumeric characters only
        Regexp(r"^[A-Za-z0-9 ]+$", error="User name must contain alphanumeric characters only")
        ))
    # email column - string data value, cannot be null and must be unique
    email = fields.String(required=True, validate=And(
        # email must be between 5 and 120 characters long
        Length(min=5, max=120, error="Email must be 5 and 120 characters long"),
        # email must contain alphanumeric characters only
        Regexp(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,4}$", error="Invalid email format. Email must contain alphanumeric characters only")
        ))
    # dob column - string data value
    date = fields.String(validate=
        # date must be written as dd/mm/yyyy only
        Regexp(r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$", error="Date must written as dd/mm/yyyy only")
        )
    # password column - string data value and cannot be null, must be at 
    # least 8 characters long, have at least one letter and one number
    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Password must be at least 8 characters long, have at least one letter and one number"))

    # Meta class to define the fields to be included in the schema 
    class Meta:
        # fields to be included in the schema
        fields = ("id", "name", "user_name", "email", "dob", "password", "is_admin", "posts", "comments", "likes", "events", "attending")


# user_schema object set to call UserSchema class
# we do not want to pass the password back to the user so we exclude it
# to handle a single user object
# must exclude user so it does not make a never ending loop
user_schema = UserSchema(exclude=["password"])
# to handle a list user objects
users_schema = UserSchema(many=True, exclude=["password"])