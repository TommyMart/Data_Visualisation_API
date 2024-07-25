# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

# Imports from local files
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from utils import authorise_as_admin
from models.event import Event
from models.attending import Attending

# Define the Blueprint for the invoices
invoice_bp = Blueprint("invoices", __name__,
                       url_prefix="/<int:attending_id>/invoice")

# GET route to fetch a specific invoice for a specific event and attending ID
# /<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id>


@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
# Protect the route with JWT
@jwt_required()
# Define the function to fetch a specific invoice
def fetch_specific_invoice(event_id, attending_id, invoice_id):
    try:
        # Check if the event exists
        event_exists = db.session.query(Event.id).filter_by(
            id=event_id).scalar() is not None
        # If event does not exist
        if not event_exists:
            # Return error message to client and status code
            return {"error": f"Event with id '{event_id}' does not exist."}, 404

        # Check if the attending exists
        attending_exists = db.session.query(Attending.id).filter_by(
            id=attending_id).scalar() is not None
        # If attending does not exist
        if not attending_exists:
            # Return error message to client
            return {"error": f"Attending with id '{attending_id}' does not exist."}, 404

        # Check if the specific invoice exists for the given event and attending ID
        invoice = db.session.query(Invoice).filter_by(
            event_id=event_id, attendee_id=attending_id, id=invoice_id).first()
        # If invoice exists
        if invoice:
            # Return the invoice data and status code
            return invoice_schema.dump(invoice), 200
        # If invoice does not exist
        else:
            # Return error message to client and status code
            return {"error": f"Invoice with id '{invoice_id}' not found for event with id '{event_id}' and attending id '{attending_id}'"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# GET route to fetch all invoices for a specific event and attending ID
# /<int:event_id>/attending/<int:attending_id>/invoice/


@invoice_bp.route("/")
# Protect the route with JWT
@jwt_required()
# Define the function to fetch all invoices for a specific event and attending ID
def fetch_event_attending(event_id, attending_id):
    try:
        # Check if the event exists
        event_exists = db.session.query(Event.id).filter_by(
            id=event_id).scalar() is not None
        # If event does not exist
        if not event_exists:
            # Return error message to client and staus code
            return {"error": f"Event with id '{event_id}' does not exist."}, 404

        # Check if the attending exists
        attending_exists = db.session.query(Attending.id).filter_by(
            id=attending_id).scalar() is not None
        # If attending does not exist
        if not attending_exists:
            # Return error message to client and status code
            return {"error": f"Attending with id '{attending_id}' does not exist."}, 404

        # Fetch all invoices for the given event and attending ID
        stmt = db.select(Invoice).filter_by(
            event_id=event_id, attendee_id=attending_id).order_by(Invoice.timestamp.desc())
        # Get all invoices linked to the event and attending ID
        invoices = db.session.scalars(stmt).all()
        # If invoices exist
        if invoices:
            # Return the invoices and status code
            return invoices_schema.dump(invoices), 200
        # If invoices do not exist
        else:
            # Return error message to client and status code
            return {"error": f"No invoices found for event with id '{event_id}' and attending id '{attending_id}"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# POST route to create a new invoice for a specific event and attending ID
# /events/<int:event_id>/attending/<int:attending_id>/invoice/


@invoice_bp.route("/", methods=["POST"])
# Protect the route with JWT
@jwt_required()
# Define the function to create a new invoice
def new_invoice(event_id, attending_id):
    try:
        # Get the request data from the payload
        body_data = request.get_json()
        # Check if the event exists
        event_exists = db.session.query(Event.id).filter_by(
            id=event_id).scalar() is not None
        # If event does not exist
        if not event_exists:
            # Return error message to client and status code
            return {"error": f"Event with id '{event_id}' does not exist."}, 404

        # Check if the attendee exists
        attending_exists = db.session.query(Attending.id).filter_by(
            id=attending_id, event_id=event_id).scalar() is not None
        # If attendee does not exist
        if not attending_exists:
            # Return error message to client and status code
            return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404

        # Create a new invoice instance and get the data from the payload
        invoice = Invoice(
            total_cost=body_data.get("total_cost"),
            timestamp=datetime.now(),
            event_id=event_id,
            attendee_id=attending_id
        )
        # Add the invoice to the session
        db.session.add(invoice)
        # Commit the session to the DB
        db.session.commit()
        # Return the invoice data and status code
        return invoice_schema.dump(invoice), 201
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# DELETE route to delete a specific invoice, only Admins can delete invoices
# /events/<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id>


@invoice_bp.route("/<int:invoice_id>", methods=["DELETE"])
# Protect the route with JWT
@jwt_required()
# Define the function to delete an invoice
def delete_invoice(event_id, attending_id, invoice_id):
    try:
        # Check if the event exists
        event_exists = db.session.query(Event.id).filter_by(
            id=event_id).scalar() is not None
        # If event does not exist
        if not event_exists:
            # Return error message to client and status code
            return {"error": f"Event with id '{event_id}' does not exist."}, 404

        # Check if the attendee exists
        attending_exists = db.session.query(Attending.id).filter_by(
            id=attending_id, event_id=event_id).scalar() is not None
        # If attendee does not exist
        if not attending_exists:
            # Return error message to client and status code
            return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404

        # Fetch the invoice
        stmt = db.select(Invoice).filter_by(
            id=invoice_id, event_id=event_id, attendee_id=attending_id)
        # Get the invoice
        invoice = db.session.scalar(stmt)

        # If invoice exists
        if invoice:
            # check whether the user is an admin
            is_admin = authorise_as_admin()
            # if the user is not an admin they cannot delete an invoice
            if not is_admin:
                # return error message to client and status code
                return {"error": "User unorthorised to perform this request"}, 403
            # delete invoice data
            db.session.delete(invoice)
            # commit session to DB
            db.session.commit()
            # return query success message to client
            return {"message": f"Invoice '{invoice.id}' deleted successfully"}, 200
        # if event, attending or invoice does not exist
        else:
            # return error message to client and status code
            return {"error": f"Invoice with id '{invoice_id}' not found for event with id '{event_id}' and attending id '{attending_id}'"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500

# PUT or PATCH - Update an invoice - Only Admins can update invoices
# /events/<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id>


@invoice_bp.route("/<int:invoice_id>", methods=["PUT", "PATCH"])
# Protect the route with JWT
@jwt_required()
# Define the function to update an invoice
def update_invoice(invoice_id, event_id, attending_id):
    try:
        # Get the request data from the payload
        body_data = invoice_schema.load(request.get_json())

        # Check if the event exists
        event_exists = db.session.query(Event.id).filter_by(
            id=event_id).scalar() is not None
        # If event does not exist
        if not event_exists:
            # Return error message to client and status code
            return {"error": f"Event with id '{event_id}' does not exist."}, 404

        # Check if the attendee exists
        attendee_exists = db.session.query(Attending.id).filter_by(
            id=attending_id, event_id=event_id).scalar() is not None

        # If attendee does not exist
        if not attendee_exists:
            # Return error message to client and status code
            return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404

        # Fetch the invoice
        stmt = db.select(Invoice).filter_by(
            id=invoice_id, event_id=event_id, attendee_id=attending_id)
        # Get the invoice
        invoice = db.session.scalar(stmt)
        # If invoice exists
        if invoice:
            # check whether the user is an admin
            is_admin = authorise_as_admin()
            # if the user is not an admin they cannot update the invoice
            if not is_admin:
                # return error message to client and status code
                return {"error": "User unorthorised to perform this request"}, 403
            # update the invoice data or keep the same if no data is passed
            invoice.total_cost = body_data.get(
                "total_cost") or invoice.total_cost
            invoice.timestamp = body_data.get("timestamp") or invoice.timestamp
            # session already added so just need to commit
            db.session.commit()
            # return updated invoice data and status code
            return invoice_schema.dump(invoice), 200
        # if event, attending or invoice does not exist
        else:
            # return error message to client and status code
            return {"error": f"Invoice with id '{invoice_id}' not found for event with id '{event_id}' and attending id '{attending_id}'"}, 404
    except Exception as e:
        # Handle unexpected errors
        return {"error": str(e)}, 500
