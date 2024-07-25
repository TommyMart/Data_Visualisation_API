# External Libraries
from marshmallow import fields

# Imports from local files
from init import db, ma

# Table model for the likes table in the DB


class Like(db.Model):
    try:
        # Name of the table
        __tablename__ = "likes"

        # Table Attributes
        # ID column - Integer data type and primary key of the "likes" table
        id = db.Column(db.Integer, primary_key=True)

        # Foreign Keys
        # User ID column - Foreign key referencing the ID attribute from the users table
        # Cannot be null because a like must be associated with a user
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        # Post ID column - Foreign key referencing the ID attribute from the posts table
        # Cannot be null because a like must be associated with a post
        post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
        # Comment ID column - Foreign key referencing the ID attribute from the comments 
        # table (comment_id is commented out for now)
        # comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)

        # Relationships
        # Link to the User model - A user can have multiple likes
        user = db.relationship("User", back_populates="likes")
        # Link to the Post model - A post can have multiple likes
        post = db.relationship("Post", back_populates="likes")
        # Link to the Comment model (comment_id is commented out for now)
        # comment = db.relationship("Comment", back_populates="likes")
    except Exception as e:
        # Handle unexpected errors
        print(str(e)), 500

# Schema instance from Marshmallow - Convert DB objects to 
# Python objects and vice versa


class LikeSchema(ma.Schema):
    try:
        # A like is associated with a single user (nested object)
        user = fields.Nested("UserSchema", only=["name", "email"])
        # A like is associated with a single post (nested object)
        post = fields.Nested("PostSchema", only=["title", "id"])

        # Meta class to define the fields to be included in the schema
        class Meta:
            # Fields to be included in the schema
            fields = ("id", "user", "post")
    except Exception as e:
        # Handle unexpected errors
        print(str(e)), 500


# Schema for a single like object
like_schema = LikeSchema()
# Schema for a list of like objects
likes_schema = LikeSchema(many=True)
