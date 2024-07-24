# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
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

# post/<int:post_id>/comments - GET - Fetch a specific comment on a post
@comments_bp.route("/<int:comment_id>")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch a specific comment
def fetch_single_comments(post_id, comment_id):
    # check if the post exists
    post_exists = db.session.query(Post.id).filter_by(id=post_id).scalar() is not None
    # if post does not exist
    if not post_exists:
        # return error message to client and status code
        return {"error": f"Post with id '{post_id}' does not exist."}, 404
    
    # find the comment in the DB with the id = comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    # fetch the comment from the DB with correct id
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment: 
        # return the comment data and status code       
        return comment_schema.dump(comment), 200
    # if comment does not exist
    else:
        # return error message to client and status code
        return {"error": f"Comment with id {comment_id} not found"}, 404


# post/<int:post_id>/comments - GET - Fetch all comments on a post
@comments_bp.route("/")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch all comments on a post
def fetch_comments(post_id):
    # check if the post exists
    post_exists = db.session.query(Post.id).filter_by(id=post_id).scalar() is not None
    # if post does not exist
    if not post_exists:
        # return error message to client and status code
        return {"error": f"Post with id '{post_id}' does not exist."}, 404
    
    # fetch the post from the DB
    stmt = db.select(Post).filter_by(id=post_id)
    # Get the post
    post = db.session.scalars(stmt)
    # if post exists
    if post: 
        # fetch all comments linked to the post
        stmt = db.select(Comment).order_by(Comment.id.asc())
        # Get all comments linked to the post
        users = db.session.scalars(stmt)
        # return the comments and status code
        return comments_schema.dump(users), 200
    # if post does not exist
    else:
        # return error message to client and status code
        return {"error": f"Post with id {post_id} not found"}, 404

# post/<int:post_id>/comments
# Create comment route on a Post
@comments_bp.route("/", methods=["POST"])
# Protect the route with JWT
@jwt_required()
# Define the function to create a comment
def create_comment(post_id):
    # get the comment object from the payload
    body_data = comment_schema.load(request.get_json())
    # fetch the post with the correct id - post_id (passed in url)
    stmt = db.select(Post).filter_by(id=post_id)
    # get the post
    post = db.session.scalar(stmt)
    # if card exists
    if post:
        # create an instance of the Comment model
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
# Protect the route with JWT
@jwt_required()
# Define the function to delete a comment
def delete_comment(post_id, comment_id):
    # find the comment from the DB
    stmt = db.select(Comment).filter_by(id=comment_id)
    # get the comment
    comment = db.session.scalar(stmt)
    # if comment exists
    if comment:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the post
        if not is_admin and str(comment.user_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        # delete the comment
        db.session.delete(comment)
        # commit the session
        db.session.commit()
        # return an error messafe to the client and status code
        return {"message": f"Comment '{comment.content}' deleted successfully"}, 200
    # else
    else:
        # return an error message to the client and status code
        return {"error": f"Comment with id {comment_id} not found"}, 404

# /posts/post_id/comments/comment_id - PUT/PATCH - Update a comment
@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
# Protect the route with JWT
@jwt_required()
# Define the function to update a comment
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
            return {"error": "Only the user account holder can update it"}, 403
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