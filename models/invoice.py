
# External Libraries
from marshmallow import fields

# Imports from local files
from init import db, ma

# Table model for the invoices table in the DB
class Invoice(db.Model):
    # Table Name
    __tablename__ = "invoices"

    # Table Attributes
    # id - integer data value and primary key of "invoices" table
    id = db.Column(db.Integer, primary_key=True)
    # total_cost - float data value and default value of 0.00
    total_cost = db.Column(db.Float, default=0.00)
    # timestamp - date data value
    timestamp = db.Column(db.Date)

    # Foreign Keys
    # event_id foreign key references id attribute from events table
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    # attendee_id foreign key references id attribute from attending table
    attendee_id = db.Column(db.Integer, db.ForeignKey("attending.id"), nullable=False)

    # Relationships
    # A invoice can now have a event field
    event = db.relationship("Event", back_populates="invoice")
    # A invoice can now have a attending field
    attending = db.relationship("Attending", back_populates="invoice")
    

# Schema for the invoices table
class InvoiceSchema(ma.Schema):
    # A single invoice can only belong to a single event
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    # A single invoice can only belong to a single attending
    attending = fields.Nested("AttendingSchema", only=["seat_section", "total_tickets", "user"])

    # Meta class to define the fields to be returned
    class Meta:
        # fields to be returned
        fields = ( "id", "total_cost", "time_stamp", "event_id", "attendee_id", "event", "attending" )

# create an instance of the schema
invoice_schema = InvoiceSchema()
# create an instance of the schema for multiple invoices
invoices_schema = InvoiceSchema(many=True)