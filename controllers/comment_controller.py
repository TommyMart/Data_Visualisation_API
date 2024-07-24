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

# A comment cannot exist without a post, it belongs to a post, so we register the comments_bp Blueprint to posts_bp (posts blueprint), and therefore it will take on its "/posts" url_prefix, so we don't need /posts in the URL.
# /<int:post_id>/comments
comments_bp = Blueprint("comments", __name__,
                        url_prefix="/<int:post_id>/comments")

# No need to create a fetch all comments route because it would have no purpose, we only want all the comments linked to one post, which we get when fetching posts.

# GET - Fetch a specific comment on a post
# /<int:post_id>/comments/<int:comment_id>


@comments_bp.route("/<int:comment_id>")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch a specific comment
def fetch_single_comment(post_id, comment_id):
    # Check if the post exists
    post_exists = db.session.query(Post.id).filter_by(
        id=post_id).scalar() is not None
    # If post does not exist
    if not post_exists:
        # Return error message to client and status code
        return {"error": f"Post with id '{post_id}' does not exist."}, 404

    # Find the comment in the DB with the id = comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    # Fetch the comment from the DB with correct id
    comment = db.session.scalar(stmt)
    # If comment exists
    if comment:
        # Return the comment data and status code
        return comment_schema.dump(comment), 200
    # If comment does not exist
    else:
        # Return error message to client and status code
        return {"error": f"Comment with id {comment_id} not found"}, 404

# GET - Fetch all comments on a post
# /<int:post_id>/comments


@comments_bp.route("/")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch all comments on a post
def fetch_comments(post_id):
    # Check if the post exists
    post_exists = db.session.query(Post.id).filter_by(
        id=post_id).scalar() is not None
    # If post does not exist
    if not post_exists:
        # Return error message to client and status code
        return {"error": f"Post with id '{post_id}' does not exist."}, 404

    # Fetch all comments linked to the post
    stmt = db.select(Comment).filter_by(
        post_id=post_id).order_by(Comment.id.asc())
    comments = db.session.scalars(stmt)
    # Return the comments and status code
    return comments_schema.dump(comments), 200

# POST - Create a comment on a post
# /<int:post_id>/comments


@comments_bp.route("/", methods=["POST"])
# Protect the route with JWT
@jwt_required()
# Define the function to create a comment
def create_comment(post_id):
    # Get the comment object from the payload
    body_data = comment_schema.load(request.get_json())
    # Fetch the post with the correct id - post_id (passed in URL)
    stmt = db.select(Post).filter_by(id=post_id)
    # Get the post
    post = db.session.scalar(stmt)
    # If post exists
    if post:
        # Create an instance of the Comment model
        comment = Comment(
            content=body_data.get("content"),
            timestamp=datetime.now(),
            post=post,
            user_id=get_jwt_identity()
        )
        # Add and commit the session
        db.session.add(comment)
        db.session.commit()
        # Return the created comment and status code
        return comment_schema.dump(comment), 201
    # If post does not exist
    else:
        # Return an error message to the client and status code
        return {"error": f"Post with id {post_id} not found"}, 404

# DELETE - Delete a comment
# /<int:post_id>/comments/<int:comment_id>


@comments_bp.route("/<int:comment_id>", methods=["DELETE"])
# Protect the route with JWT
@jwt_required()
# Define the function to delete a comment
def delete_comment(post_id, comment_id):
    # Find the comment from the DB
    stmt = db.select(Comment).filter_by(id=comment_id)
    # Get the comment
    comment = db.session.scalar(stmt)
    # If comment exists
    if comment:
        # Check whether the user is an admin
        is_admin = authorise_as_admin()
        # If the user is not the owner of the post
        if not is_admin and str(comment.user_id) != get_jwt_identity():
            return {"error": "User unauthorized to perform this request"}, 403
        # Delete the comment
        db.session.delete(comment)
        # Commit the session
        db.session.commit()
        # Return a success message to the client and status code
        return {"message": f"Comment '{comment.content}' deleted successfully"}, 200
    # If comment does not exist
    else:
        # Return an error message to the client and status code
        return {"error": f"Comment with id {comment_id} not found"}, 404

# PUT/PATCH - Update a comment
# /<int:post_id>/comments/<int:comment_id> -


@comments_bp.route("/<int:comment_id>", methods=["PUT", "PATCH"])
# Protect the route with JWT
@jwt_required()
# Define the function to update a comment
def update_comment(post_id, comment_id):
    # Get the values from the payload
    body_data = comment_schema.load(request.get_json())
    # Find the comment in the DB with the id = comment_id
    stmt = db.select(Comment).filter_by(id=comment_id)
    # Fetch the comment from the DB with correct id
    comment = db.session.scalar(stmt)
    # If comment exists
    if comment:
        # If the user is not the owner of the post
        if str(comment.user_id) != get_jwt_identity():
            return {"error": "Only the user account holder can update it"}, 403
        # Update the fields
        comment.content = body_data.get("content") or comment.content
        # Commit the session
        db.session.commit()
        # Return the updated comment data and status code
        return comment_schema.dump(comment), 200
    # If comment does not exist
    else:
        # Return error message to client and status code
        return {"error": f"Comment with id {comment_id} not found"}, 404
