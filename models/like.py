
# External Libraries
from marshmallow import fields

# Imports from local files
from init import db, ma

# Create likes Model 
# child of Model class
class Like(db.Model):
    # name the table
    __tablename__ = "likes"

    # Define attributes of the table and their datatypes
    id = db.Column(db.Integer, primary_key=True)

    # foreign keys
    # user_id foreign key references id attribute from users table 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # post_id foreign key references id attribute from posts table 
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    # comment_id foreign key references id attribute from comments table 
    # comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)

    # Gain access to the entire model's data instead of just the id foriegn key
    # Who made the post, who commented on the post etc. must be done on the other
    # side to create the connection
    user = db.relationship("User", back_populates="likes")
    # A post can now have a comments field
    post = db.relationship("Post", back_populates="likes")
    # A post can now have a comments field
    # comment = db.relationship("Comment", back_populates="likes")

# Create a schema for the likes model
class LikeSchema(ma.Schema):
    # Only one user can like a post, so it is a single object
    user = fields.Nested("UserSchema", only=["name", "email"])
    # Only one post can be liked, so it is a single object
    post = fields.Nested("PostSchema", only=["title", "id"])

    # Meta class to define the fields to be returned
    class Meta:
        fields = ("id", "user", "post")

# create an instance of the schema
like_schema =  LikeSchema()
# create an instance of the schema for multiple likes
likes_schema = LikeSchema(many=True)