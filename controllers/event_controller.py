# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
from init import db
from models.event import Event, event_schema, events_schema
from controllers.attending_controller import attending_bp
from utils import authorise_as_admin

# Define the Blueprint for the events
events_bp = Blueprint("events", __name__, url_prefix="/events")
# Register the attending_bp blueprint to the events_bp
events_bp.register_blueprint(attending_bp)

# GET - Fetch all events
# /events/


@events_bp.route("/")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch all events
def get_all_events():
    try:
        # Get all records from the events table ordered by date in descending order
        stmt = db.select(Event).order_by(Event.date.desc())
        # Retrieves the query results as individual 'Event' objects
        events = db.session.scalars(stmt)
        # Serialises the list of "Event" objects into JSON so that it can be returned to client
        return events_schema.dump(events), 200
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# GET - Fetch single event
# /events/<int:event_id>


@events_bp.route("/<int:event_id>")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch a single event
def get_single_event(event_id):
    try:
        # Select a single iteration of the Event Model from the DB
        stmt = db.select(Event).filter_by(id=event_id)
        # Retrieve the row where the ids match
        event = db.session.scalar(stmt)
        # If event object exists
        if event:
            # Serialise into JSON and return to client
            return event_schema.dump(event), 200
        # If does not exist
        else:
            # Return message and error status code
            return {"error": f"Event with id {event_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# GET - Fetch event/s by partial event_title
# /events/search/<string:event_title>


@events_bp.route("/search/<string:event_title>")
# Protect the route with JWT
@jwt_required()
# Define the function to search for events by title
def search_event_by_name(event_title):
    try:
        # Construct the LIKE pattern for partial matching
        like_pattern = f"%{event_title}%"
        # Perform a case-insensitive search using ilike (case-insensitive LIKE)
        stmt = db.select(Event).filter(Event.title.ilike(like_pattern))
        # Retrieve all matching events
        events = db.session.scalars(stmt).all()
        # If events are found
        if events:
            # Return the serialised data
            return events_schema.dump(events), 200
        # If no events are found
        else:
            # Return an error message and status code
            return {"error": f"No events found matching '{event_title}'"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# POST - Create a new event
# /events/


@events_bp.route("/", methods=["POST"])
# Protect the route with JWT
@jwt_required()
# Define the function to create a new event
def create_event():
    try:
        # Get data from payload
        body_data = event_schema.load(request.get_json(), partial=True)
        # Create new Event Model instance and populate with data
        event = Event(
            title=body_data.get("title"),
            description=body_data.get("description"),
            date=body_data.get("date"),
            ticket_price=body_data.get("ticket_price"),
            event_admin_id=get_jwt_identity()
        )
        # Add and commit to DB
        db.session.add(event)
        db.session.commit()
        # Return the serialised data
        return event_schema.dump(event), 201
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# DELETE - Delete an event
# /events/<int:event_id> -


@events_bp.route("/<int:event_id>", methods=["DELETE"])
# Protect the route with JWT
@jwt_required()
# Define the function to delete an event
def delete_event(event_id):
    try:
        # Select the event with the correct id
        stmt = db.select(Event).filter_by(id=event_id)
        # Retrieve the event
        event = db.session.scalar(stmt)
        # If event exists
        if event:
            # check whether the user is an admin
            is_admin = authorise_as_admin()
            # if the user is not the owner of the post
            if not is_admin and str(event.event_admin_id) != get_jwt_identity():
                return {"error": "User unauthorized to perform this request"}, 403
            # Delete the event from the session
            db.session.delete(event)
            # Commit the session to the DB
            db.session.commit()
            # Return a success message
            return {"message": f"Event '{event.title}' deleted successfully"}, 200
        # If event does not exist
        else:
            # Return an error message and status code 404
            return {"error": f"Event with id {event_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# PUT or PATCH - Update an event
# /events/<int:event_id>


@events_bp.route("/<int:event_id>", methods=["PUT", "PATCH"])
# Protect the route with JWT
@jwt_required()
# Define the function to update an event
def update_event(event_id):
    try:
        # Load the request data from the payload
        body_data = event_schema.load(request.get_json())
        # Select the event with the correct id
        stmt = db.select(Event).filter_by(id=event_id)
        # Retrieve the event
        event = db.session.scalar(stmt)
        # If event exists
        if event:
            # If the user is not the creator of the event
            if str(event.event_admin_id) != get_jwt_identity():
                # Return an error message and status code 403
                return {"error": "Only the creator of an event can update it"}, 403
            # Update the event data or leave as is if not provided
            event.title = body_data.get("title") or event.title
            event.description = body_data.get(
                "description") or event.description
            event.date = body_data.get("date") or event.date
            event.ticket_price = body_data.get(
                "ticket_price") or event.ticket_price
            # Session already added so just need to commit
            db.session.commit()
            # Return the updated event data
            return event_schema.dump(event), 200
        # If event does not exist
        else:
            # Return an error message and status code 404
            return {"error": f"Event {event_id} not found"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500
