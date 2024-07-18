
# External Libraries
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError

# Imports from local files
from init import db, ma
from models.user import User

# Constants
# do not want the values to change so we use a tuple
VALID_SEAT_SECTIONS = ( "General Addmission", "Section A", "Section B", "Section C", "VIP" ) 

# Define a maximum number of tickets per user per event_id
MAX_TICKETS_PER_USER = 5
MAX_TICKETS_PER_EMAIL = 5

# Attending Table
class Attending(db.Model):

    # Table Name
    __tablename__ = "attending"

    # Table Attributes
    id = db.Column(db.Integer, primary_key=True)
    total_tickets = db.Column(db.Integer, default=1)
    seat_section = db.Column(db.String, default="General Admission")
    timestamp = db.Column(db.Date)

    # Foreign Keys
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    attending_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = db.relationship("User", back_populates="attending")
    event = db.relationship("Event", back_populates="attending", cascade="all, delete")
    invoice = db.relationship("Invoice", back_populates="attending", cascade="all, delete")

# Attending Schema
class AttendingSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email", "is_admin"])
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    invoice = fields.Nested("InvoiceSchema", only=["total_cost"])
    
    # Validation
    seat_section = fields.String(validate=OneOf(VALID_SEAT_SECTIONS), error="Please enter a valid seating section")

    @validates("total_tickets")
    def validate_max_tickets(self, value):
        if value > MAX_TICKETS_PER_USER:
            raise ValidationError(f"Maximum {MAX_TICKETS_PER_USER} tickets allowed per user per event")

    @validates("user")
    def validate_email_tickets_limit(self, value):
        email = value.get("email")
        if email:
            # Query the database to count tickets already purchased by this email
            stmt = db.session.query(db.func.sum(Attending.total_tickets)).join(Attending.user).filter(User.email == email).scalar()
            if stmt and stmt + value["total_tickets"] > MAX_TICKETS_PER_EMAIL:
                raise ValidationError(f"Maximum {MAX_TICKETS_PER_EMAIL} tickets allowed per email address")

    @validates("seat_section")
    def limit_general_admission(self, value):
        if value == VALID_SEAT_SECTIONS[0]:
            # check DB if there are any Section A seat_sections
            # go into attending table and count the number of Section A seat_sections
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[0])
            count = db.session.scalar(stmt)
            # if exists check 
            if count > 5:
                raise ValidationError("No more General Admission tickets available, please select a different seat section")

    
    @validates("seat_section")
    def limit_section_A(self, value):
        if value == VALID_SEAT_SECTIONS[1]:
            # check DB if there are any Section A seat_sections
            # go into attending table and count the number of Section A seat_sections
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[1])
            count = db.session.scalar(stmt)
            # if exists check 
            if count > 5:
                raise ValidationError("No more Section A tickets available, please select a different seat section")
        

    @validates("seat_section")
    def limit_section_B(self, value):
        if value == VALID_SEAT_SECTIONS[2]:
            # check DB if there are any Section B seat_sections
            # go into attending table and count the number of Section B seat_sections
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[2])
            count = db.session.scalar(stmt)
            # if exists check 
            if count > 5:
                raise ValidationError("No more Section B tickets available, please select a different seat section")
        
    @validates("seat_section")
    def limit_section_C(self, value):
        if value == VALID_SEAT_SECTIONS[3]:
            # check DB if there are any Section C seat_sections
            # go into attending table and count the number of Section C seat_sections
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[3])
            count = db.session.scalar(stmt)
            # if exists check 
            if count > 5:
                raise ValidationError("No more Section C tickets available, please select a different seat section")
        

    @validates("seat_section")
    def limit_vip(self, value):
        if value == VALID_SEAT_SECTIONS[4]:
            # check DB if there are any VIP seat_sections
            # go into attending table and count the number of VIP seat_sections
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[4])
            count = db.session.scalar(stmt)
            # if exists check 
            if count > 2:
                raise ValidationError("No more VIP tickets available, please select a different seat section")
    
    
    class Meta:
        fields = ( "id", "total_tickets", "seat_section", "timestamp", "event_id", "attending_id", "user", "event", "invoice" )

attending_schema = AttendingSchema()
attendings_schema = AttendingSchema(many=True)