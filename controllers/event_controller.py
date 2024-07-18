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

events_bp = Blueprint("events", __name__, url_prefix="/events")
events_bp.register_blueprint(attending_bp)

# /events/ - GET - fetch all events
@events_bp.route("/")
@jwt_required()
def get_all_events():
    # get all records from the events table ordered by date in descending order
    stmt = db.select(Event).order_by(Event.date.desc())
    # retrieves the query results as individual 'Event' objects
    events = db.session.scalars(stmt)
    # serialises the list of "Event" objects into JSON so that it can be returned
    # to client 
    return events_schema.dump(events)

# /events/<int:event_id> - GET - fetch single event
@events_bp.route("/<int:event_id>")
@jwt_required()
def get_single_event(event_id):
    # select a single interation of the Event Model from the DB, filter the data to 
    # find an entry where the event_id sent in the payload matches an id in the DB
    stmt = db.select(Event).filter_by(id=event_id)
    # retrieve the row where the ids match
    event = db.session.scalar(stmt)
    # if event object exists
    if event:
        # serialise into JSON and return to client
        return event_schema.dump(event)
    # if does not exist
    else:
        # return message and error status code
        return {"error": f"Event with id {event_id} not found"}, 404
    

# /events/ - POST - create a new event
@events_bp.route("/", methods=["POST"])
@jwt_required()
def create_event():
    # get data from payload 
    body_data = event_schema.load(request.get_json(), partial=True)
    # create new Event Model instance
    event = Event(
        title = body_data.get("title"),
        description = body_data.get("description"),
        date = body_data.get("date"),
        ticket_price = body_data.get("ticket_price"),
        event_admin_id = get_jwt_identity()
    )

    db.session.add(event)
    db.session.commit()

    return event_schema.dump(event)

# /events/<int:event_id> - DELETE - delete an event
@events_bp.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the post
        if not is_admin and str(event.event_admin_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        db.session.delete(event)
        db.session.commit()
        return {"message": f"Event '{event.title}' deleted successfully"}
    else:
        return {"error": f"Event with id {event_id} not found"}, 404
    
# /events/<int:event_id> - PUT or PATCH - update an event data
@events_bp.route("/<int:event_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_event(event_id):
    body_data = event_schema.load(request.get_json())

    stmt = db.select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        # if the user is not the owner of the post
        if str(event.event_admin_id) != get_jwt_identity():
            return {"error": "Only the creator of a post can update it"}, 403
        event.title = body_data.get("title") or event.title
        event.description = body_data.get("description") or event.description
        event.date = body_data.get("date") or event.date
        event.ticket_price = body_data.get("ticket_price") or event.ticket_price
        # session already added so just need to commit
        db.session.commit()

        return event_schema.dump(event)

    else:
        return {"error": f"Event {event_id} not found"}
    
