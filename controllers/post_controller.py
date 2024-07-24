# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
from init import db
from controllers.comment_controller import comments_bp
from controllers.like_controller import likes_bp
from models.post import Post, post_schema, posts_schema
from models.user import User
from utils import authorise_as_admin

# Create a Blueprint for post-related routes
posts_bp = Blueprint("posts", __name__, url_prefix="/posts")

# Register the comments and likes blueprints with the posts blueprint
posts_bp.register_blueprint(comments_bp)
posts_bp.register_blueprint(likes_bp)

# Route to fetch all posts


@posts_bp.route("/", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def get_all_posts():
    """
    Fetch all posts from the database, ordered by date in descending order.
    """
    stmt = db.select(Post).order_by(
        Post.date.desc())  # Prepare SQL query to fetch all posts
    posts = db.session.scalars(stmt)  # Execute the query
    # Return the posts with status code 200
    return posts_schema.dump(posts), 200

# Route to fetch a single post by post_id


@posts_bp.route("/<int:post_id>", methods=["GET"])
@jwt_required()  # Protect the route with JWT authentication
def get_single_post(post_id):
    """
    Fetch a single post by post_id from the database.
    """
    stmt = db.select(Post).filter_by(
        id=post_id)  # Prepare SQL query to fetch post by ID
    post = db.session.scalar(stmt)  # Execute the query
    if post:
        # Return the post with status code 200
        return post_schema.dump(post), 200
    else:
        # Return error if post not found
        return {"error": f"Post with id {post_id} not found"}, 404

# Route to create a new post


@posts_bp.route("/", methods=["POST"])
@jwt_required()  # Protect the route with JWT authentication
def new_post():
    """
    Create a new post and add it to the database.
    """
    body_data = post_schema.load(
        request.get_json())  # Load and validate request data
    post = Post(
        title=body_data.get("title"),
        content=body_data.get("content"),
        date=datetime.now(),
        location=body_data.get("location"),
        image_url=body_data.get("image_url"),
        user_id=get_jwt_identity()  # Get the user ID from the JWT token
    )
    db.session.add(post)  # Add the new post to the session
    db.session.commit()  # Commit changes to the database
    # Return the created post with status code 201
    return post_schema.dump(post), 201

# Route to delete a post by post_id


@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()  # Protect the route with JWT authentication
def delete_post(post_id):
    """
    Delete a post from the database.
    """
    stmt = db.select(Post).filter_by(
        id=post_id)  # Prepare SQL query to fetch post by ID
    post = db.session.scalar(stmt)  # Execute the query
    if post:
        is_admin = authorise_as_admin()  # Check if the current user is an admin
        # Ensure user is authorized to delete the post
        if not is_admin and str(post.user_id) != get_jwt_identity():
            # Return forbidden error if unauthorized
            return {"error": "User unauthorized to perform this request"}, 403
        db.session.delete(post)  # Delete the post
        db.session.commit()  # Commit changes to the database
        # Return success message with status code 200
        return {"message": f"Post '{post.title}' deleted successfully"}, 200
    else:
        # Return error if post not found
        return {"error": f"Post with id {post_id} not found"}, 404

# Route to update a post by post_id


@posts_bp.route("/<int:post_id>", methods=["PUT", "PATCH"])
@jwt_required()  # Protect the route with JWT authentication
def update_post(post_id):
    """
    Update a post's details.
    """
    body_data = post_schema.load(
        request.get_json(), partial=True)  # Load and validate request data
    # Prepare SQL query to fetch post by ID
    stmt = db.select(Post).filter_by(id=post_id)
    post = db.session.scalar(stmt)  # Execute the query
    if post:
        # Ensure the user is authorized to update the post
        if str(post.user_id) != get_jwt_identity():
            # Return forbidden error if unauthorized
            return {"error": "Only the creator of a post can update it"}, 403
        # Update the post fields as provided in the request
        post.title = body_data.get("title") or post.title
        post.content = body_data.get("content") or post.content
        post.date = body_data.get("date") or post.date
        post.location = body_data.get("location") or post.location
        post.image_url = body_data.get("image_url") or post.image_url
        db.session.commit()  # Commit changes to the database
        # Return the updated post with status code 200
        return post_schema.dump(post), 200
    else:
        # Return error if post not found
        return {"error": f"Post with id {post_id} not found"}, 404
