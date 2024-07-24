# External Libraries
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma

# Comment model class


class Comment(db.Model):
    # Name of the table
    __tablename__ = "comments"

    # Table Attributes
    # ID column - Integer data type and primary key of the "comments" table
    id = db.Column(db.Integer, primary_key=True)
    # Content column - String data type and cannot be null
    content = db.Column(db.String, nullable=False)
    # Timestamp column - Date data type
    timestamp = db.Column(db.Date)

    # Foreign Keys
    # User ID column - Foreign key referencing the ID attribute from the users table
    # Cannot be null because a comment must be associated with a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Post ID column - Foreign key referencing the ID attribute from the posts table
    # Cannot be null because a comment must be associated with a post
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Relationships
    # Link to the User model - A comment is associated with a single user
    user = db.relationship("User", back_populates="comments")
    # Link to the Post model - A comment is associated with a single post
    post = db.relationship("Post", back_populates="comments")

# Create a schema for the Comment model


class CommentSchema(ma.Schema):
    
    # A comment is associated with a single user (nested object)
    user = fields.Nested("UserSchema", only=["name", "email"])
    # Prevent recursion by excluding comments from the post schema
    # A comment is associated with a single post (nested object)
    post = fields.Nested("PostSchema", exclude=["comments"])

    # Validation
    # Content column - String data type and cannot be null
    content = fields.String(validate=And(
        # Content must be less than 400 characters long
        Length(max=400, error="A comment must be less than 400 characters long"),
        # Content must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$",
               error="A comment must contain alphanumeric characters only")
    ))

    # Meta class to define the fields to be included in the schema
    class Meta:
        # Fields to be included in the schema
        fields = ("id", "content", "timestamp", "user", "post")


# Schema instance for a single comment object
comment_schema = CommentSchema()
# Schema instance for a list of comment objects
comments_schema = CommentSchema(many=True)
