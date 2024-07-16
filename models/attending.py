# 
from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

# do not want the values to change so we use a tuple
VALID_SEAT_SECTIONS = ( "General Addmission", "Section A", "Section B", "Section C", "VIP" ) 

# TABLE
class Attending(db.Model):
    # Table Name
    __tablename__ = "attending"
    # Table Attributes
    id = db.Column(db.Integer, primary_key=True)
    total_tickets = db.Column(db.Integer, default=1)
    seat_section = db.Column(db.String, default="General Admission")
    timestamp = db.Column(db.Date)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    attending_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Relationships
    user = db.relationship("User", back_populates="attending")
    event = db.relationship("Event", back_populates="attending", cascade="all, delete")
    invoice = db.relationship("Invoice", back_populates="attending")

# SCHEMA
class AttendingSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    invoice = fields.Nested("InvoiceSchema", only=["total_cost"])
    
    # VALIDATION
    seat_section = fields.String(validate=OneOf(VALID_SEAT_SECTIONS), error="Please enter a valid seating section")

    class Meta:
        fields = ( "id", "total_tickets", "seat_section", "timestamp", "event_id", "attending_id", "user", "event", "invoice" )

attending_schema = AttendingSchema()
attendings_schema = AttendingSchema(many=True)