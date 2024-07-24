
# External Libraries
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Imports from local files
from init import db, ma


# Table model for the posts table in the DB
class Post(db.Model):
    # name of the table
    __tablename__ = "posts"

    # Table Attributes
    # id column - integer data value and primary key of "posts" table
    id = db.Column(db.Integer, primary_key=True)
    # title column - string data value and cannot be null
    title = db.Column(db.String, nullable=False)
    # content column - string data value
    content = db.Column(db.String)
    # date column - date data value
    date = db.Column(db.Date)
    # location column - string data value
    location = db.Column(db.String)
    # image_url column - string data value
    image_url = db.Column(db.String)

    # Foreign Keys
    # foreign key referencing the id value from the users table in the DB, 
    # it cannot be nullable because a post must be created by a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    # access users.id information from users accessed using foreign key
    # with sqlalchemy. Must use model name to back_populate variable name
    # user is now a nested object inside posts, not a column attribute of the table 
    # A user can have multiple 'posts' 
    user = db.relationship("User", back_populates="posts")
    # A post can have multiple comments that we can fetch
    # When deleting a post, delete all the comments as well (cascade = all, delete)
    # A single comment will belong to a single card
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete")
    likes = db.relationship("Like", back_populates="post", cascade="all, delete")

# schema instance from marshmallow - convert db objects to python objects
class PostSchema(ma.Schema):

    # marshmallow does not know how to serialise/deserialise nested objects
    # such as the user object so we must tell it that user is a nested field
    # and it has the same object as the UserSchema model

    # A post can have only one user (nested object)
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    # A single post can have multiple comments (list)
    comments = fields.List(fields.Nested("CommentSchema", exclude=["post"]))
    # A single post can have multiple likes (list)
    likes = fields.List(fields.Nested("LikeSchema", exclude=["post"]))

    # Validation
    # title column - string data value and cannot be null
    title = fields.String(required=True, validate=And(
        # title must be at least 3 characters long
        Length(min=3, error="Title must be at least 3 characters long"),
        # title must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$", error="Title must contain alphanumeric characters only")
        ))
    # content column - string data value
    content = fields.String(validate=And(
        # content must be less than 400 characters long
        Length(max=400, error="Post content must be less than 400 characters long"),
        # content must contain alphanumeric characters only
        Regexp("^[A-Za-z0-9 ]+$", error="Post content must contain alphanumeric characters only")
    ))
    # date column - date data value
    location = fields.String(validate=And(
        # location must be between 3 and 100 characters long
        Length(min=3, max=100, error="Location must be between 3 and 100 characters long"),
        # location must contain alpha characters only
        Regexp("^[A-Za-z ]+$", error="Location must contain alpha characters only")
        ))
    # image_url column - string data value
    image_url = fields.String(validate=And(
        # image_url must be between 5 and 150 characters long
        Length(min=5, max=150, error="URL must be between 5 and 150 characters long"),
        # image_url must be a valid URL
        Regexp("https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}", error="Please enter a valid URL")
    ))

    # Meta class to define the fields to be returned
    class Meta:
        # fields to be included in the schema
        fields = ( "id", "title", "content", "image_url", "date", "location", "user", "comments", "likes" )
        # Marshmallow keeps the order when . dump
        ordered =  True

# schema for one post
post_schema = PostSchema()
# schema for a list of post objects
posts_schema = PostSchema(many=True)
