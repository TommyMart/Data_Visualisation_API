
# External Libraries
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Imports from local files
from init import db, ma


# TABLE
class Post(db.Model):
    # Table Name
    __tablename__ = "posts"

    # Table Attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date = db.Column(db.Date)
    location = db.Column(db.String)
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

# payload will look like below
    # { 
    #     id: 1,
    #     title: Post 1,
    #     content: "Post content",
    #     date: "...",
    #     user_id: 1,
    #     user: {
    #         id: 1,
    #         name: "User 1",
    #         email: "user1@email.com"
    # },
    #     comments: [
    #       {
    #           id: 1,
    #           comment: "comment 1"
    #       },
    #       {
    #           id: 2,
    #           comment: "comment 2"
    #       }
    #       ]
    # }

# SCHEMA
class PostSchema(ma.Schema):

    # marshmallow does not know how to serialise/deserialise nested objects
    # such as the user object so we must tell it that user is a nested field
    # it has the same object as the UserSchema model, we only need name and id
    # to populate who the post is by and link to user profile via users.id
    # a post only has a single user so it is not fields.List
    user = fields.Nested("UserSchema", only=["id", "name", "email"])
    # A single card can have multiple comments so is a list
    # We don't need the card information again because we on the post
    
    comments = fields.List(fields.Nested("CommentSchema", exclude=["post"]))
    likes = fields.List(fields.Nested("LikeSchema", exclude=["post"]))

    # Validation
    title = fields.String(required=True, validate=And(
        Length(min=3, error="Title must be at least 3 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Title must contain alphanumeric characters only")
        ))
    content = fields.String(validate=And(
        Length(max=400, error="Post content must be less than 400 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Post content must contain alphanumeric characters only")
    ))
    location = fields.String(validate=And(
        Length(min=3, max=100, error="Location must be between 3 and 100characters long"),
        Regexp("^[A-Za-z ]+$", error="Location must contain alpha characters only")
        ))
    image_url = fields.String(validate=And(
        Length(min=5, max=150, error="URL must be between 5 and 150 characters long"),
        Regexp("https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}", error="Please enter a valid URL")
    ))


    class Meta:
        
        fields = ( "id", "title", "content", "image_url", "date", "location", "user", "comments", "likes" )
        # Marshmallow keeps the order when . dump
        ordered =  True

# schema for one post
post_schema = PostSchema()
# schema for a list of post objects
posts_schema = PostSchema(many=True)
