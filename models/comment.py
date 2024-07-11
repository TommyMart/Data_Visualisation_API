from init import db, ma
from marshmallow import fields

# Create comments the model 
# child of Model class
class Comment(db.Model):
    # name the table
    __tablename__ = "comments"

    # Define attributes of the table and their datatypes
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Date)

    # foreign keys
    # user_id foreign key references id attribute from users table 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # post_id foreign key references id attribute from posts table 
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Get the data of the user who made the comment
    # links to User model to the comments field of the user model,
    # that is made in the user model
    user = db.relationship("User", back_populates="comments")
    # A post can now have a comments field
    post = db.relationship("Post", back_populates="comments")

class CommentSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    # prevent looping by excluding comments because we're already on the 
    # comment
    post = fields.Nested("PostSchema", exclude=["comments"])

    class Meta:
        fields = ("id", "content", "timestamp", "user", "comments")

comment_schema =  CommentSchema()
comments_schema = CommentSchema(many=True)