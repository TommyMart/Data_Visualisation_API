from init import db, ma
from marshmallow import fields

from models.attending import Attending


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
    attending = db.relationship("Attending", back_populates="event")


class EventSchema(ma.Schema):
    # pass event admin name and email address
    user = fields.Nested("UserSchema", only=["name", "email"])
    attending = fields.List(fields.Nested("AttendingSchema", only=["event_id", "seat_number", "total_tickets", "user"]))

    # define a schema - structure of the DB
    class Meta:
        fields = ( "id", "title", "description", "date", "ticket_price", "event_admin_id", "user", "attending" )

event_schema = EventSchema()
events_schema = EventSchema(many=True)