# External Libraries
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Imports from local files
from init import db, ma

# Table model for the posts table in the DB


class Post(db.Model):
    # Name of the table
    __tablename__ = "posts"

    # Table Attributes
    # ID column - Integer data type and primary key of the "posts" table
    id = db.Column(db.Integer, primary_key=True)
    # Title column - String data type and cannot be null
    title = db.Column(db.String, nullable=False)
    # Content column - String data type
    content = db.Column(db.String)
    # Date column - Date data type
    date = db.Column(db.Date)
    # Location column - String data type
    location = db.Column(db.String)
    # Image URL column - String data type
    image_url = db.Column(db.String)

    # Foreign Keys
    # Foreign key referencing the ID value from the users table in the DB
    # It cannot be null because a post must be created by a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    # Link to the User model - A user can have multiple posts
    user = db.relationship("User", back_populates="posts")
    # Link to the Comment model - A post can have multiple comments
    # When deleting a post, delete all the comments as well (cascade="all, delete")
    comments = db.relationship(
        "Comment", back_populates="post", cascade="all, delete")
    # Link to the Like model - A post can have multiple likes
    likes = db.relationship(
        "Like", back_populates="post", cascade="all, delete")

# Schema instance from Marshmallow - Convert DB objects to Python 
# objects and vice versa


class PostSchema(ma.Schema):

    # Relationships
    # A post can have only one user (nested object)
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    # A single post can have multiple comments (list)
    comments = fields.List(fields.Nested("CommentSchema", exclude=["post"]))
    # A single post can have multiple likes (list)
    likes = fields.List(fields.Nested("LikeSchema", exclude=["post"]))

    # Validation
    # Title column - String data type and cannot be null
    title = fields.String(required=True, validate=And(
        # Title must be at least 3 characters long
        Length(min=3, error="Title must be at least 3 characters long"),
        # Title must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$",
               error="Title must contain alphanumeric characters only")
    ))
    # Content column - String data type
    content = fields.String(validate=And(
        # Content must be less than 400 characters long
        Length(max=400, error="Post content must be less than 400 characters long"),
        # Content must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$",
               error="Post content must contain alphanumeric characters only")
    ))
    # Location column - String data type
    location = fields.String(validate=And(
        # Location must be between 3 and 100 characters long
        Length(min=3, max=100,
               error="Location must be between 3 and 100 characters long"),
        # Location must contain alphabetic characters only
        Regexp("^[A-Za-z ]+$",
               error="Location must contain alphabetic characters only")
    ))
    # Image URL column - String data type
    image_url = fields.String(validate=And(
        # Image URL must be between 5 and 150 characters long
        Length(min=5, max=150, error="URL must be between 5 and 150 characters long"),
        # Image URL must be a valid URL
        Regexp(
            r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}",
            error="Please enter a valid URL"
        )
    ))

    # Meta class to define the fields to be included in the schema
    class Meta:
        # Fields to be included in the schema
        fields = ("id", "title", "content", "image_url", "date",
                  "location", "user", "comments", "likes")
        # Marshmallow keeps the order when .dump
        ordered = True


# Schema for a single post object
post_schema = PostSchema()
# Schema for a list of post objects
posts_schema = PostSchema(many=True)
