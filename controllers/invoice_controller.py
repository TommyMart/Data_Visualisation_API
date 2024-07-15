from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.invoice import Invoice, invoice_schema, invoices_schema


invoice_bp = Blueprint("invoices", __name__, url_prefix="/<int:attending_id>/invoice")

# /events/<int:event_id>/attending/<int:attending_id>/invoice/<int:invoice_id>
# GET - fetch a single invoice
@invoice_bp.route("/<int:invoice_id>")
@jwt_required()
def get_single_invoice(event_id, attending_id, invoice_id):
    stmt = db.select(Invoice).filter_by(id=invoice_id, attendee_id=attending_id)
    invoice = db.session.scalar(stmt)

    if invoice:
        return invoice_schema.dump(invoice), 200
    
    else:
        return {"error": f"Invoice with id '{invoice_id}' not found"}, 404

# /events/<int:event_id>/attending/<int:attending_id>/invoice/ - POST -
# create an invoice
@invoice_bp.route("/", methods=["POST"])
@jwt_required()
def new_invoice(event_id, attending_id):
    body_data = request.get_json()
    
    invoice = Invoice(
        total_cost = body_data.get("total_cost"),
        timestamp = datetime.now(),
        event_id = body_data.get("event_id"),
        attendee_id = body_data.get("attendee_id")
    )

    db.session.add(invoice)
    db.session.commit()

    return invoice_schema.dump(invoice), 201