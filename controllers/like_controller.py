# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
from init import db
from models.like import Like, like_schema, likes_schema
from models.post import Post
from utils import authorise_as_admin

# Blueprint for like-related routes, registered under the posts blueprint
likes_bp = Blueprint("likes", __name__, url_prefix="/<int:post_id>/likes")

# Route to fetch all likes on a post
# /<int:post_id>/likes/


@likes_bp.route("/", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def fetch_all_likes_on_post(post_id):
    try:
        """
        Fetch all likes associated with a specific post.
        """
        stmt = db.select(Like).filter_by(
            post_id=post_id)  # Prepare SQL query to fetch likes by post ID
        likes = db.session.scalars(stmt)  # Execute the query
        if likes:
            # Return the likes with status code 
            return likes_schema.dump(likes), 200
        else:
            # Return error if post not found
            return {"error": f"Post with id {post_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to create a like on a post
# /<int:post_id>/likes/


@likes_bp.route("/", methods=["POST"])
@jwt_required()  # Protect the route with JWT authentication
def create_like(post_id):
    try:
        """
        Create a new like associated with a specific post.
        """
        stmt = db.select(Post).filter_by(
            id=post_id)  # Prepare SQL query to fetch post by ID
        post = db.session.scalar(stmt)  # Execute the query
        if post:
            like = Like(
                post=post,  # Associate the like with the post
                user_id=get_jwt_identity()  # Get the user ID from the JWT token
            )
            db.session.add(like)  # Add the new like to the session
            db.session.commit()  # Commit changes to the database
            # Return the created like with status code 
            return like_schema.dump(like), 201
        else:
            # Return error if post not found
            return {"error": f"Post with id {post_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# Route to delete a like by like_id
# /<int:post_id>/likes/<int:like_id>


@likes_bp.route("/<int:like_id>", methods=["DELETE"])
@jwt_required()  # Protect the route with JWT authentication
def delete_like(post_id, like_id):
    try:
        """
        Delete a like associated with a specific post.
        """
        stmt = db.select(Like).filter_by(
            id=like_id)  # Prepare SQL query to fetch like by ID
        like = db.session.scalar(stmt)  # Execute the query
        if like:
            is_admin = authorise_as_admin()  # Check if the current user is an admin
            # Ensure user is authorized to delete the like
            if not is_admin and str(like.user_id) != get_jwt_identity():
                # Return forbidden error if unauthorized
                return {"error": "User unauthorized to perform this request"}, 403
            db.session.delete(like)  # Delete the like
            db.session.commit()  # Commit changes to the database
            # Return success message with status code 
            return {"message": f"Like '{like.id}' deleted successfully"}, 200
        else:
            # Return error if like not found
            return {"error": f"Like with id {like_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500
