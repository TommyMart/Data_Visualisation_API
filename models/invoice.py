from init import db, ma
from marshmallow import fields

class Invoice(db.Model):
    __tablename__ = "invoices"

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.Float, default=0.00)
    timestamp = db.Column(db.Date)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    attendee_id = db.Column(db.Integer, db.ForeignKey("attending.id"), nullable=False)

    event = db.relationship("Event", back_populates="invoice")
    attending = db.relationship("Attending", back_populates="invoice")
    


class InvoiceSchema(ma.Schema):
    
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    attending = fields.Nested("AttendingSchema", only=["seat_number", "total_tickets", "user"])

    # define a schema - structure of the DB
    class Meta:
        fields = ( "id", "total_cost", "time_stamp", "event_id", "attendee_id", "event", "attending" )

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)