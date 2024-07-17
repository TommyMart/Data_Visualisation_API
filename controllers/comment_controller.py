from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.comment import Comment, comment_schema, comments_schema
from models.post import Post 
from utils import authorise_as_admin

# a comment cannot exist without a card, it belongs to a card, so can
# register Blueprint to posts_bp (posts blueprint), and therefore it will
# take on its "/posts" url_prefix, so we don't need /posts.
# /<int:post_id>/comments
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:post_id>/comments")

# no need to create a fetch all comments route because it would have no purpose,
# we only want all the comments linked to one post, which we get when fetching posts,
# which we get when fetching a Post. 



# Create comment route on a Post
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(post_id):
    # get the comment object from the payload
    body_data = comment_schema.load(request.get_json())
    # fetch the post with the correct id - post_id (passed in url)
    stmt = db.select(Post).filter_by(id=post_id)
    post = db.session.scalar(stmt)
    # if card exists
    if post:
        # Create an instance of the Comment model
        comment = Comment(
            content = body_data.get("content"),
            timestamp = datetime.now(),
            # already passed post_id
            post = post,
            # use get_jwt_identity to get the logged in user.id
            user_id = get_jwt_identity()
        )
        # Add and commit the session
        db.session.add(comment)
        db.session.commit()
        # return the created commit 
        return comment_schema.dump(comment), 201
    #else:
    else:
        # return an error that the post_id does not exist
        return {"error": f"Post with id {post_id} not found"}, 404

# Delete Comment - /posts/post_id/comments/comment_id
# only need comment_id because the rest of the route is taken care of
# in the posts_bp and comments_bp Blueprint url prefixes
@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(post_id, comment_id):
    # fetch the comment from the DB
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the post
        if not is_admin and str(comment.user_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        # delete comment
        db.session.delete(comment)
        db.session.commit()
        # return a message
        return {"message": f"Comment '{comment.content}' deleted successfully"}
    # else
    else:
        # return error saying comment does not exist
        return {"error": f"Comment with id {comment_id} not found"}, 404

# Update comment - /posts/post_id/comments/comment_id
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_comment(post_id, comment_id):
    # get the values from the payload
    body_data = comment_schema.load(request.get_json())
    # find the comment in the DB with the id = comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    # fetch the comment from the DB with correct id
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # if the user is not the owner of the post
        if str(comment.user_id) != get_jwt_identity():
            return {"error": "Only the creator of a post can update it"}, 403
        # update the fields
        # only field we can update - with what ever the user has sent in payload
        # if data in the content payload, update, if not, leave as is
        comment.content = body_data.get("content") or comment.content
        # commit (already fetched so don't need to add)
        db.session.commit()
        # return a response to the client 
        return comment_schema.dump(comment)
    # else
    else:
        # return error saying comment does not exist
        return {"error": f"Comment id with {comment_id} not found"}, 404