# External Libraries
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Imports from local files
from init import db, ma
from models.attending import Attending
from models.invoice import Invoice


# Table model for the events table in the DB
class Event(db.Model):
    # name of the table
    __tablename__ = "events"

    # Tabel attributes
    # id column - integer data value and primary key of "events" table
    id = db.Column(db.Integer, primary_key=True)
    # title column - string data value
    title = db.Column(db.String)
    # description column - string data value
    description = db.Column(db.String)
    # date column - date data value
    date = db.Column(db.Date)
    # ticket_price column - float data value and default value of 0.00
    ticket_price = db.Column(db.Float, default=0.00)
    
    # Forieng Keys
    # event_admin_id foreign key references id attribute from users table
    event_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Relationships
    # A event can have a user field
    user = db.relationship("User", back_populates="events")
    # A event can have a attending field
    attending = db.relationship("Attending", back_populates="event", cascade="all, delete")
    # A event can have a invoice field
    invoice = db.relationship("Invoice", back_populates="event", cascade="all, delete")

class EventSchema(ma.Schema):
    # A event can have only one user (nested object)
    user = fields.Nested("UserSchema", only=["name", "email"])
    # A single event can have multiple attending (list)
    attending = fields.List(fields.Nested("AttendingSchema", only=["event_id", "seat_section", "total_tickets", "user"]))
    # A single event can have multiple invoices (list)
    invoice = fields.List(fields.Nested("InvoiceSchema", only=["total_cost"]))

    # Validation
    # title - string data value and cannot be null
    date = fields.String(validate=
        # date must be written as dd/mm/yyyy only
        Regexp(r"^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$", error="Date must written as dd/mm/yyyy only")
        )
    
    # Meta class to define the fields to be returned
    class Meta:
        # fields to be returned
        fields = ( "id", "title", "description", "date", "ticket_price", "event_admin_id", "user", "attending", "invoice")

# create an instance of the schema
event_schema = EventSchema()
# create an instance of the schema for multiple events
events_schema = EventSchema(many=True)