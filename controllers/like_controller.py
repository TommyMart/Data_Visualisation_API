from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.like import Like, like_schema, likes_schema
from models.post import Post 
from utils import authorise_as_admin

# a like cannot exist without a post, it belongs to a post, so we can
# register Blueprint to posts_bp (posts blueprint), and therefore it will
# take on its "/posts" url_prefix, so we don't need to include "/posts".
# /<int:post_id>/likes
likes_bp = Blueprint("likes", __name__, url_prefix="/<int:post_id>/likes")

# no need to create a fetch all likes route because it would have no purpose,
# we only want all the likes linked to one post, which we get when fetching posts.

# post/<int:post_id>/likes - GET - fetch all likes on a post
@likes_bp.route("/")
@jwt_required()
def fetch_all_likes_on_post(post_id):
    # fetch the post with the correct id - post_id (passed in url)
    stmt = db.select(Like).filter_by(post_id=post_id)
    likes = db.session.scalars(stmt)

    if likes: 
        
        return likes_schema.dump(likes)
    
    else:
        return {"error": f"Post with id {post_id} not found"}, 404

# Create like route
@likes_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(post_id):
    # get the post object from the payload
    body_data = request.get_json()
    # fetch the post with the correct id - post_id (passed in url)
    stmt = db.select(Post).filter_by(id=post_id)
    post = db.session.scalar(stmt)
    # if card exists
    if post:
        # Create an instance of the Like model
        like = Like(
            # already passed post_id
            post = post,
            # use get_jwt_identity to get the logged in user.id
            user_id = get_jwt_identity()
        )
        # Add and commit the session
        db.session.add(like)
        db.session.commit()
        # return the created commit 
        return like_schema.dump(like), 201
    #else:
    else:
        # return an error that the post_id does not exist
        return {"error": f"Post with id {post_id} not found"}, 404

# Delete Like - /posts/post_id/likes/like_id
# only need like_id because the rest of the route is taken care of
# in the posts_bp and likes_bp Blueprint url prefixes
@likes_bp.route("/<int:like_id>", methods=["DELETE"])
@jwt_required()
def delete_like(post_id, like_id):
    # fetch the like from the DB
    stmt = db.select(Like).filter_by(id=like_id)
    like = db.session.scalar(stmt)
    # if like exists
    if like:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the post
        if not is_admin and str(like.user_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        # delete like
        db.session.delete(like)
        db.session.commit()
        # return a message
        return {"message": f"Like '{like.id}' deleted successfully"}
    # else
    else:
        # return error saying comment does not exist
        return {"error": f"Comment with id {like_id} not found"}, 404

