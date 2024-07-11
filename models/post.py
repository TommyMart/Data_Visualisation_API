
# import sqlalchemy and marshmallow form init.py
from init import db, ma
from marshmallow import fields

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
    # allow us to fetch all the posts made by a user
    user = db.relationship("User", back_populates="posts")


class PostSchema(ma.Schema):

    # marshmallow does not know how to serialise/deserialise nested objects
    # such as the user object so we must tell it that user is a nested field
    # it has the same object as the UserSchema model, we only need name and id
    # to populate who the post is by and link to user profile via users.id
    # a post only has a single user so it is not fields.List
    user = fields.Nested("UserSchema", only=["id", "name"])

    class Meta:
        # can access users.id via user object foreign key
        fields = ( "id", "title", "content", "image_url", "date", "location", "user" )


# schema for one post
post_schema = PostSchema()
# schema for a list of post objects
posts_schema = PostSchema(many=True)

