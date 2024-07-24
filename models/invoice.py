# External Libraries
from marshmallow import fields

# Imports from local files
from init import db, ma

# Table model class for the invoices table in the DB


class Invoice(db.Model):
    # Name of the table
    __tablename__ = "invoices"

    # Table Attributes
    # ID column - Integer data type and primary key of the "invoices" table
    id = db.Column(db.Integer, primary_key=True)
    # Total cost column - Float data type with a default value of 0.00
    total_cost = db.Column(db.Float, default=0.00)
    # Timestamp column - Date data type
    timestamp = db.Column(db.Date)

    # Foreign Keys
    # Event ID column - Foreign key referencing the ID attribute from the 
    # events table
    # Cannot be null because an invoice must be associated with an event
    event_id = db.Column(db.Integer, db.ForeignKey(
        "events.id"), nullable=False)
    # Attendee ID column - Foreign key referencing the ID attribute 
    # from the attending table
    # Cannot be null because an invoice must be associated with an attendee
    attendee_id = db.Column(db.Integer, db.ForeignKey(
        "attending.id"), nullable=False)

    # Relationships
    # Link to the Event model - An invoice is associated with a single event
    event = db.relationship("Event", back_populates="invoice")
    # Link to the Attending model - An invoice is associated with a single 
    # attending record
    attending = db.relationship("Attending", back_populates="invoice")

# Schema instance from Marshmallow - Convert DB objects to 
# Python objects and vice versa


class InvoiceSchema(ma.Schema):
    # An invoice is associated with a single event (nested object)
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    # An invoice is associated with a single attending record (nested object)
    attending = fields.Nested("AttendingSchema", only=[
                              "seat_section", "total_tickets", "user"])

    # Meta class to define the fields to be included in the schema
    class Meta:
        # Fields to be included in the schema
        fields = ("id", "total_cost", "timestamp", "event_id",
                  "attendee_id", "event", "attending")


# Schema for a single invoice object
invoice_schema = InvoiceSchema()
# Schema for a list of invoice objects
invoices_schema = InvoiceSchema(many=True)
