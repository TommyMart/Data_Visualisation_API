# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
from models.attending import Attending, attending_schema, attendings_schema
from models.event import Event
from controllers.invoice_controller import invoice_bp
from utils import authorise_as_admin
from init import db

attending_bp = Blueprint("attending", __name__, url_prefix="/<int:event_id>/attending")
attending_bp.register_blueprint(invoice_bp)

# no need to fetch all attending all events, only fetch all attending a specific event
# we can get all attending event by fetching an event

# /<int:event_id>/attending - GET - fetch all attending an event
@attending_bp.route("/")
@jwt_required()
def fetch_event_attending(event_id):

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404
    
    stmt = db.select(Attending).filter_by(event_id=event_id).order_by(Attending.timestamp.desc())
    attendees = db.session.scalars(stmt).all()

    if attendees:

        return attendings_schema.dump(attendees)
    
    else: 
        return {"error": f"No attendees found for event with id '{event_id}"}, 404

# /<int:event_id>/attending/<int:attendee_id> - GET - fetch a specific attendee for an event
@attending_bp.route("/<int:attending_id>")
@jwt_required()
def fetch_specific_attendee(event_id, attending_id):
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404
    
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attending_id)
    attendee = db.session.scalar(stmt)

    if attendee:
        return attending_schema.dump(attendee)
    else:
        return {"error": f"No attendee found with id '{attending_id}' for event with id '{event_id}'"}, 404

# /<int:event_id>/attending - POST - attending an event
@attending_bp.route("/", methods=["POST"])
@jwt_required()
def attending_event(event_id):
    body_data = attending_schema.load(request.get_json(), partial=True)

    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        attending = Attending(
            total_tickets = body_data.get("total_tickets"),
            seat_section = body_data.get("seat_section"),
            timestamp = datetime.now(),
            event = event,
            attending_id = get_jwt_identity()
        )

        db.session.add(attending)
        db.session.commit()
        return attending_schema.dump(attending), 201
    
    else:
        return {"error": f"Event with id '{event_id}' not found"}, 404
        


# # /<int:event_id>/attending/<int:attending_id> - DELETE - only require
# # the attending id because event id has been fetched in the url_prefix
# @attending_bp.route("/<int:attending_id>", methods=["DELETE"])
# @jwt_required()
# def delete_attending(event_id, attending_id):

#     # Check if the event exists
#     event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
#     if not event_exists:
#         return {"error": f"Event with id '{event_id}' does not exist."}, 404
    
#     # Fetch the attending record with the correct attending_id and event_id
#     stmt = db.session(Attending).filter_by(id=attending_id, event_id=event_id)
#     attending = db.session.scalar(stmt)

#     if attending:
#         # check whether the user is an admin 
#         is_admin = authorise_as_admin()
#         # if the user is not the owner of the post
#         if not is_admin and str(attending.user_id) != get_jwt_identity():
#             return {"error": "User unorthorised to perform this request"}, 403
#         db.session.delete(attending)
#         db.session.commit()
#         return {"message": f"Attending record with id '{attending_id}' deleted successfully"}

#     else:
#         return {f"Attendee with id '{attending_id}' not found for event with id '{event_id}'"}, 404
    

# Update comment - /posts/post_id/comments/comment_id
@attending_bp.route("/<int:attendee_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_attendee(event_id, attendee_id):

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404
    

    body_data = attending_schema.load(request.get_json(), partial=True)
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attendee_id)
    attending = db.session.scalar(stmt)

    
    
    

    if attending:
        # if the user is not the owner of the post
        if str(attending.attending_id) != get_jwt_identity():
            return {"error": "Only the creator of a post can update it"}, 403
        attending.total_tickets = body_data.get("total_tickets") or attending.total_tickets
        attending.seat_section = body_data.get("seat_section") or attending.seat_section
        attending.timestamp = body_data.get("time_stamp") or attending.timestamp
    
        db.session.commit()
        return attending_schema.dump(attending)
    
    else:
        return {"error": f"Attending with id '{attendee_id}' not found"}
    

@attending_bp.route("/<int:attendee_id>", methods=["DELETE"])
@jwt_required()
def delete_attending(event_id, attendee_id):

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404
    
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attendee_id)
    attendee = db.session.scalar(stmt)
    # fetch the attending from the DB
    stmt = db.select(Attending).filter_by(id=attendee_id)
    attending = db.session.scalar(stmt)
    # if attending exists
    if attending:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the attending
        if not is_admin and str(attending.user_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        # delete attending
        db.session.delete(attending)
        db.session.commit()
        # return a message
        return {"message": f"Attending id '{attending.id}' deleted successfully"}
    # else
    else:
        # return error saying attending does not exist
        return {"error": f"Attending with id {attendee_id} not found"}, 404