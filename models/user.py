# External Libraries
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma
from models.like import Like


# Create model class extended from the SQLAlchemy model class


class User(db.Model):

    # Table name
    __tablename__ = "users"

    # Table attributes
    # ID column - Integer data type and primary key of the "users" table
    id = db.Column(db.Integer, primary_key=True)
    # Name column - String data type, cannot be null
    name = db.Column(db.String, nullable=False)
    # User name column - String data type, cannot be null
    user_name = db.Column(db.String, nullable=False)
    # Password column - String data type, cannot be null
    password = db.Column(db.String, nullable=False)
    # Email column - String data type, cannot be null, must be unique
    email = db.Column(db.String, nullable=False, unique=True)
    # Date of Birth column - Date data type
    dob = db.Column(db.Date)
    # Admin status column - Boolean data type, default is False
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    # Link to the Post model - A user can have 0 or multiple posts
    posts = db.relationship(
        "Post", back_populates="user", cascade="all, delete")
    # Link to the Comment model - A user can have 0 or multiple comments
    comments = db.relationship(
        "Comment", back_populates="user", cascade="all, delete")
    # Link to the Like model - A user can have 0 or multiple likes
    likes = db.relationship(
        "Like", back_populates="user", cascade="all, delete")
    # Link to the Event model - A user can have 0 or multiple events
    events = db.relationship(
        "Event", back_populates="user", cascade="all, delete")
    # Link to the Attending model - A user can have 0 or multiple attendances
    attending = db.relationship(
        "Attending", back_populates="user", cascade="all, delete")

# Schema instance from Marshmallow - Convert DB objects to Python objects and vice versa


class UserSchema(ma.Schema):

    # A user can have zero or more posts; list of PostSchema objects
    posts = fields.List(fields.Nested("PostSchema", exclude=["user"]))
    # A user can have zero or more comments; list of CommentSchema objects
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))
    # A user can have zero or more likes; list of LikeSchema objects
    likes = fields.List(fields.Nested("LikeSchema", exclude=["user"]))
    # A user can have zero or more events; list of EventSchema objects
    events = fields.List(fields.Nested("EventSchema", exclude=["user"]))
    # A user can have zero or more attendances; list of AttendingSchema objects
    attending = fields.List(fields.Nested("AttendingSchema", exclude=["user"]))

    # Validation
    # Name column - String data type, cannot be null
    name = fields.String(required=True, validate=And(
        # Name must be between 3 and 50 characters long
        Length(min=3, max=50, error="Name must be between 3 and 50 characters long"),
        # Name must contain alphanumeric characters only
        Regexp(r"^[A-Za-z0-9 ]+$",
               error="Name must contain alphanumeric characters only")
    ))
    # User name column - String data type, cannot be null
    user_name = fields.String(required=True, validate=And(
        # User name must be between 3 and 50 characters long
        Length(min=3, max=50,
               error="User name must be between 3 and 50 characters long"),
        # User name must contain alphanumeric characters only
        Regexp(r"^[A-Za-z0-9 ]+$",
               error="User name must contain alphanumeric characters only")
    ))
    # Email column - String data type, cannot be null, must be unique
    email = fields.String(required=True, validate=And(
        # Email must be between 5 and 120 characters long
        Length(min=5, max=120,
               error="Email must be between 5 and 120 characters long"),
        # Email must be in a valid format
        Regexp(
            r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,4}$", error="Invalid email format")
    ))
    # Date of Birth column - String data type
    date = fields.String(validate=# Date must be in dd/mm/yyyy format
                         Regexp(
                             r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$", error="Date must be in dd/mm/yyyy format")
                         )
    # Password column - String data type, cannot be null, must be at least 8 characters long, 
    # include at least one letter and one number
    password = fields.String(required=True, validate=Regexp(
        "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", error="Password must be at least 8 characters long, including at least one letter and one number"))

    # Meta class to define the fields to be included in the schema
    class Meta:
        # Fields to be included in the schema
        fields = ("id", "name", "user_name", "email", "dob", "password",
                  "is_admin", "posts", "comments", "likes", "events", "attending")


# Schema instances for handling user objects
# Exclude password field for security reasons
user_schema = UserSchema(exclude=["password"])
# Handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])
