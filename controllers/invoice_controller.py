# Built-in Python Libraries
from datetime import datetime

# External Libraries
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Imports from local files
from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema
from utils import authorise_as_admin
from models.event import Event
from models.attending import Attending


invoice_bp = Blueprint("invoices", __name__, url_prefix="/<int:attending_id>/invoice")

# GET route to fetch all invoices for a specific event and attending ID
# /<int:event_id>/attending/<int:attending_id>/invoice/ 
@invoice_bp.route("/")
@jwt_required()
def fetch_event_attending(event_id, attending_id):

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404
    
    
    stmt = db.select(Invoice).filter_by(event_id=event_id, attendee_id=attending_id).order_by(Invoice.timestamp.desc())
    invoices = db.session.scalars(stmt).all()

    if invoices:

        return invoices_schema.dump(invoices)
    
    else: 
        return {"error": f"No invoices found for event with id '{event_id}' and attending id '{attending_id}"}, 404

# POST route to create a new invoice for a specific event and attending ID
# /events/<int:event_id>/attending/<int:attending_id>/invoice/ 
@invoice_bp.route("/", methods=["POST"])
@jwt_required()
def new_invoice(event_id, attending_id):
    body_data = request.get_json()
    
    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Check if the attendee exists
    attendee_exists = db.session.query(Attending.id).filter_by(id=attending_id, event_id=event_id).scalar() is not None
    if not attendee_exists:
        return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404
        
    # Create a new invoice
    invoice = Invoice(
        total_cost=body_data.get("total_cost"),
        timestamp=datetime.now(),
        event_id=event_id,
        attendee_id=attending_id
    )

    db.session.add(invoice)
    db.session.commit()

    return invoice_schema.dump(invoice), 201

# DELETE route to delete an invoice for a specific event, attending ID, and invoice ID
# /events/<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id> - 
@invoice_bp.route("/<int:invoice_id>", methods=["DELETE"])
@jwt_required()
def delete_invoice(event_id, attending_id, invoice_id):

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Check if the attendee exists
    attendee_exists = db.session.query(Attending.id).filter_by(id=attending_id, event_id=event_id).scalar() is not None
    if not attendee_exists:
        return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404

    # Fetch the invoice
    stmt = db.select(Invoice).filter_by(id=invoice_id, event_id=event_id, attendee_id=attending_id)
    invoice = db.session.scalar(stmt)
    
    # If invoice exists
    if invoice:
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not and admin or the owner of the post return error
        if not is_admin and str(invoice.attendee_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        # delete invoice data
        db.session.delete(invoice)
        # commit session to DB
        db.session.commit()
        # return query success message to client
        return {"message": f"Invoice '{invoice.id}' deleted successfully"}, 200
    # if event, attending or invoice does not exist
    else:
        # return error message to client 
        return {"error": f"Invoice with id '{invoice_id}' not found for event with id '{event_id}' and attending id '{attending_id}'"}, 404
    
# /events/<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id> - 
# PUT or PATCH - update an invoice 
@invoice_bp.route("/<int:invoice_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_invoice(invoice_id, event_id, attending_id):
    body_data = invoice_schema.load(request.get_json())

    # Check if the event exists
    event_exists = db.session.query(Event.id).filter_by(id=event_id).scalar() is not None
    if not event_exists:
        return {"error": f"Event with id '{event_id}' does not exist."}, 404

    # Check if the attendee exists
    attendee_exists = db.session.query(Attending.id).filter_by(id=attending_id, event_id=event_id).scalar() is not None
    if not attendee_exists:
        return {"error": f"Attendee with id '{attending_id}' does not exist for event with id '{event_id}'"}, 404

    # Fetch the invoice
    stmt = db.select(Invoice).filter_by(id=invoice_id, event_id=event_id, attendee_id=attending_id)
    invoice = db.session.scalar(stmt)

    if invoice:
        # if the user is not the owner of the post
        # check whether the user is an admin 
        is_admin = authorise_as_admin()
        # if the user is not the owner of the post
        if not is_admin and str(invoice.attendee_id) != get_jwt_identity():
            return {"error": "User unorthorised to perform this request"}, 403
        
        invoice.total_cost = body_data.get("total_cost") or invoice.total_cost
        invoice.timestamp = body_data.get("timestamp") or invoice.timestamp
        
        # session already added so just need to commit
        db.session.commit()
        
        return invoice_schema.dump(invoice)

    else:
        return {"error": f"Invoice with id '{invoice_id}' not found for event with id '{event_id}' and attending id '{attending_id}'"}, 404