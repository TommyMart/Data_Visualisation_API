
# import sqlalchemy and marshmallow form init.py
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class Post(db.Model):
    # name of the table in DB
    __tablename__ = "posts"

    # table attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    date = db.Column(db.Date)
    location = db.Column(db.String)
    image_url = db.Column(db.String)

    # foreign key referencing the id value from the users table in the DB, 
    # it cannot be nullable because a post must be created by a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

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
        
class PostSchema(ma.Schema):

    # marshmallow does not know how to serialise/deserialise nested objects
    # such as the user object so we must tell it that user is a nested field
    # it has the same object as the UserSchema model, we only need name and id
    # to populate who the post is by and link to user profile via users.id
    # a post only has a single user so it is not fields.List
    user = fields.Nested("UserSchema", only=["id", "name"])
    # A single card can have multiple comments so is a list
    # We don't need the card information again because we on the post
    
    comments = fields.List(fields.Nested("CommentSchema", exclude=["post"]))
    likes = fields.List(fields.Nested("LikeSchema", exclude=["post"]))

    title = fields.String(required=True, validate=And(
        Length(min=3, error="Title must be at least 3 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Title must contain alphanumeric characters only")
        ))
    content = fields.String(required=True, validate=And(
        Length(max=400, error="Post content must be less than 400 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Post content must contain alphanumeric characters only")
    ))
   



    class Meta:
        
        fields = ( "id", "title", "content", "image_url", "date", "location", "user", "comments", "likes" )
        # Marshmallow keeps the order when . dump
        ordered =  True

# schema for one post
post_schema = PostSchema()
# schema for a list of post objects
posts_schema = PostSchema(many=True)
