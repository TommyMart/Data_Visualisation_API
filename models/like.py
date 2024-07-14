from init import db, ma
from marshmallow import fields

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

class LikeSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    # prevent looping by excluding likes because we're already on the 
    # likes
    post = fields.Nested("PostSchema", only=["title"])

    # define a schema - structure of the DB
    class Meta:
        fields = ("id", "user", "post")

like_schema =  LikeSchema()
likes_schema = LikeSchema(many=True)