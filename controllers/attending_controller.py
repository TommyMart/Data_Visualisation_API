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

# Create a Blueprint for the attending endpoints
attending_bp = Blueprint("attending", __name__,
                         url_prefix="/<int:event_id>/attending")
# Register the invoice blueprint within the attending blueprint
attending_bp.register_blueprint(invoice_bp)

# No need to fetch all attending all events, only fetch all attending a specific event

# GET - Fetch all attendees for a specific event
# /<int:event_id>/attending


@attending_bp.route("/")
@jwt_required()
def fetch_event_attending(event_id):
    """
    Fetch all attendees for a specific event.
    """
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(
        id=event_id).scalar() is not None

    # If the event does not exist, return a 404 error
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Query to select attendees for the event, ordered by timestamp in descending order
    stmt = db.select(Attending).filter_by(
        event_id=event_id).order_by(Attending.timestamp.desc())
    attendees = db.session.scalars(stmt).all()

    # If attendees are found, return them as a JSON response
    if attendees:
        return attendings_schema.dump(attendees)
    else:
        return {"error": f"No attendees found for event with id '{event_id}'"}, 404

# GET - Fetch a specific attendee for an event
# /<int:event_id>/attending/<int:attendee_id>


@attending_bp.route("/<int:attending_id>")
@jwt_required()
def fetch_specific_attendee(event_id, attending_id):
    """
    Fetch a specific attendee for a specific event.
    """
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(
        id=event_id).scalar() is not None

    # If the event does not exist, return a 404 error
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Query to select a specific attendee for the event
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attending_id)
    attendee = db.session.scalar(stmt)

    # If the attendee is found, return them as a JSON response
    if attendee:
        return attending_schema.dump(attendee)
    else:
        return {"error": f"No attendee found with id '{attending_id}' for event with id '{event_id}'"}, 404

# POST - Attend an event
# /<int:event_id>/attending


@attending_bp.route("/", methods=["POST"])
@jwt_required()
def attending_event(event_id):
    """
    Attend an event by creating an attendee record.
    """
    # Load request data and validate against the Attending schema
    body_data = attending_schema.load(request.get_json(), partial=True)

    # Query to select the event
    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    # If the event exists, create a new Attending object
    if event:
        # Create a new Attending object
        attending = Attending(
            total_tickets=body_data.get("total_tickets"),
            seat_section=body_data.get("seat_section"),
            timestamp=datetime.now(),
            event=event,
            attending_id=get_jwt_identity()
        )

        # Add and commit the new Attending record to the database
        db.session.add(attending)
        db.session.commit()
        # Return the new Attending record and status code
        return attending_schema.dump(attending), 201
    # if the event does not exist
    else:
        # Return an error message and status code
        return {"error": f"Event with id '{event_id}' not found"}, 404

# PUT/PATCH - Update an attendee record
# /<int:event_id>/attending/<int:attendee_id>


@attending_bp.route("/<int:attendee_id>", methods=["PUT", "PATCH"])
# Protect the route with the jwt_required() decorator
@jwt_required()
# Function to update an attendee record
def update_attendee(event_id, attendee_id):
    """
    Update an attendee record for a specific event.
    """
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(
        id=event_id).scalar() is not None

    # If the event does not exist, return a 404 error
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Load request data and validate against the Attending schema
    body_data = attending_schema.load(request.get_json(), partial=True)

    # Query to select the specific attendee
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attendee_id)
    # Fetch the attendee from the database
    attending = db.session.scalar(stmt)

    # If the attendee exists, update their information
    if attending:
        # Ensure only the attendee can update their information
        if str(attending.attending_id) != get_jwt_identity():
            # Return an error message and status code
            return {"error": "Only the attendee can update this information"}, 403

        # Update the attendee's information or keep the old value if not included
        # in the request body
        attending.total_tickets = body_data.get(
            "total_tickets") or attending.total_tickets
        attending.seat_section = body_data.get(
            "seat_section") or attending.seat_section
        attending.timestamp = body_data.get(
            "time_stamp") or attending.timestamp

        # Commit the changes to the database
        db.session.commit()
        # Return the updated attendee record and status code
        return attending_schema.dump(attending), 200
    # Return a error message if the attendee does not exist
    else:
        # Return an error message and status code
        return {"error": f"Attending with id '{attendee_id}' not found for event with id '{event_id}'"}, 404

# DELETE - Delete an attendee record
# /<int:event_id>/attending/<int:attendee_id>


@attending_bp.route("/<int:attendee_id>", methods=["DELETE"])
# Protect the route with the jwt_required() decorator
@jwt_required()
# Function to delete an attendee record
def delete_attending(event_id, attendee_id):
    """
    Delete an attendee record for a specific event.
    """
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(
        id=event_id).scalar() is not None

    # If the event does not exist, return a 404 error
    if not event_exists:
        # Return an error message and status code
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Query to select the specific attendee
    stmt = db.select(Attending).filter_by(event_id=event_id, id=attendee_id)
    # Fetch the attendee from the database
    attendee = db.session.scalar(stmt)

    # If the attendee exists, proceed with deletion
    if attendee:
        # Check if the user is an admin
        is_admin = authorise_as_admin()

        # Ensure only the attendee or an admin can delete the record
        if not is_admin and str(attendee.attending_id) != get_jwt_identity():
            return {"error": "User unauthorized to perform this request"}, 403

        # Delete the attendee record and commit the changes to the database
        db.session.delete(attendee)
        db.session.commit()

        # Return a success message
        return {"message": f"Attending id '{attendee.id}' deleted successfully"}
    # Return a 404 error if the attendee does not exist
    else:
        return {"error": f"Attendee with id '{attendee_id}' not found for event with id '{event_id}'"}, 404
