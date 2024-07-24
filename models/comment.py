# External Libraries
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma

# Create comments the model 
# child of Model class
class Comment(db.Model):
    # name the table
    __tablename__ = "comments"

    # Table Attributes
    # id column - integer data value and primary key of "comments" table
    id = db.Column(db.Integer, primary_key=True)
    # content column - string data value and cannot be null
    content = db.Column(db.String, nullable=False)
    # timestamp column - date data value
    timestamp = db.Column(db.Date)

    # Foreign Keys
    # user_id foreign key references id attribute from users table 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # post_id foreign key references id attribute from posts table 
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Gain access to the entire model's data instead of just the id foriegn key
    # Who made the post, who commented on the post etc. must be done on the other
    # side to create the connection
    # A comment can now have a user field
    user = db.relationship("User", back_populates="comments")
    # A comment can now have a post field
    post = db.relationship("Post", back_populates="comments")
   
# Create a schema for the comments model
class CommentSchema(ma.Schema):
    # Only one user can comment on a post, so it is a single object
    user = fields.Nested("UserSchema", only=["name", "email"])
    # Prevent are preventing looping by excluding comments
    # Only one post can be commented on, so it is a single object
    post = fields.Nested("PostSchema", exclude=["comments"])

    # Validation
    # content - string data value and cannot be null
    content = fields.String(validate=And(
        # content must be less than 400 characters long
        Length(max=400, error="A comment must be less than 400 characters long"),
        # content must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$", error="A comment must contain alphanumeric characters only")
    ))

    # Meta class to define the fields to be returned
    class Meta:
        fields = ("id", "content", "timestamp", "user", "post")

# create an instance of the schema
comment_schema =  CommentSchema()
# create an instance of the schema for multiple comments
comments_schema = CommentSchema(many=True)