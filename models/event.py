from init import db, ma
from marshmallow import fields

from models.attending import Attending
from models.invoice import Invoice
from marshmallow.validate import Regexp, Length, And

class Event(db.Model):
    # table name = "events"
    __tablename__ = "events"

    # attributes

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    description = db.Column(db.String)
    date = db.Column(db.Date)
    ticket_price = db.Column(db.Float, default=0.00)

    event_admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="events")
    attending = db.relationship("Attending", back_populates="event", cascade="all, delete")
    invoice = db.relationship("Invoice", back_populates="event")

class EventSchema(ma.Schema):
    # pass event admin name and email address
    user = fields.Nested("UserSchema", only=["name", "email"])
    attending = fields.List(fields.Nested("AttendingSchema", only=["event_id", "seat_number", "total_tickets", "user"]))
    invoice = fields.List(fields.Nested("InvoiceSchema", only=["total_cost"]))

    # VALIDATION
    title = fields.String(required=True, validate=And(
        Length(min=3, max=50, error="Title must be 3 and 50 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Title must contain alphanumeric characters only")
        ))
    description = fields.String(required=True, validate=And(
        Length(max=400, error="Post content must be less than 400 characters long"),
        Regexp("^[A-Za-z0-9 ]+$", error="Post content must contain alphanumeric characters only")
    ))
    date = fields.String(validate=
        Regexp("^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$", error="Date must written as dd/mm/yyyy only")
    )

    # define a schema - structure of the DB
    class Meta:
        fields = ( "id", "title", "description", "date", "ticket_price", "event_admin_id", "user", "attending", "invoice")

event_schema = EventSchema()
events_schema = EventSchema(many=True)