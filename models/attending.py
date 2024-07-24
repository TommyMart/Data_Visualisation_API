
# External Libraries
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError

# Imports from local files
from init import db, ma
from models.user import User

# Constants
# do not want the values to change so use a tuple
VALID_SEAT_SECTIONS = ( "General Addmission", "Section A", "Section B", "Section C", "VIP" ) 

# Define a maximum number of tickets per user per event_id
MAX_TICKETS_PER_USER = 5
# constant for the maximum number of tickets per email address
# MAX_TICKETS_PER_EMAIL = 5

# Attending Table Model class
class Attending(db.Model):

    # Define the table name for the Attending model
    __tablename__ = "attending"

    # Define the columns/fields for the table

    # Unique identifier for each attending record, serves as the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Total number of tickets associated with this attending record, default value is 1
    total_tickets = db.Column(db.Integer, default=1)
    # Section where the seat is located, default value is "General Admission"
    seat_section = db.Column(db.String, default="General Admission")
    # Date when the attending record was created or modified
    timestamp = db.Column(db.Date)

    # Foreign key to the 'events' table, indicates which event this record is associated with
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    # Foreign key to the 'users' table, indicates which user this record is associated with
    attending_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Define relationships to other models

    # Establish a relationship to the User model, enabling access to the user's information who is attending the event
    user = db.relationship("User", back_populates="attending")
    # Establish a relationship to the Event model, enabling access to the event's details
    event = db.relationship("Event", back_populates="attending")
    # Establish a relationship to the Invoice model, enabling access to invoices related to this attending record
    # 'cascade="all, delete"' ensures that related invoices are deleted if this attending record is deleted
    invoice = db.relationship("Invoice", back_populates="attending", cascade="all, delete")

# Schema for serialising and deserialising Attending objects
class AttendingSchema(ma.Schema):

    # Nested schema to include limited fields from the User model: name, email, and is_admin
    user = fields.Nested("UserSchema", only=["name", "email", "is_admin"])
    # Nested schema to include limited fields from the Event model: title and ticket_price
    event = fields.Nested("EventSchema", only=["title", "ticket_price"])
    # Nested schema to include limited fields from the Invoice model: total_cost
    invoice = fields.Nested("InvoiceSchema", only=["total_cost"])

    # Validate seat_section against predefined valid sections
    seat_section = fields.String(
        # use the OneOf validator to ensure the value is one of the predefined sections
        validate=OneOf(VALID_SEAT_SECTIONS), 
        # error message if the value is not one of the predefined sections
        error="Please enter a valid seating section"
    )
    # Validate total_tickets
    @validates("total_tickets")
    # Function to validate the total number of tickets
    def validate_max_tickets(self, value):
        """
        Validate the total number of tickets to ensure it does not exceed 
        the maximum allowed per user per event.
        """
        # Raise an error if the total number of tickets exceeds the maximum allowed
        if value > MAX_TICKETS_PER_USER:
            # Raise an error if the limit is exceeded
            raise ValidationError(
                f"Maximum {MAX_TICKETS_PER_USER} tickets allowed per user per event"
            )

    # this function is currently a work in progress
    # @validates("user")
    # def validate_email_tickets_limit(self, value):
    #     email = value.get("email")
    #     if email:
    #         # Query the database to count tickets already purchased by this email
    #         stmt = db.session.query(db.func.sum(Attending.total_tickets)).join(Attending.user).filter(User.email == email).scalar()
    #         if stmt and stmt + value["total_tickets"] > MAX_TICKETS_PER_EMAIL:
    #             raise ValidationError(f"Maximum {MAX_TICKETS_PER_EMAIL} tickets allowed per email address")
    
    # Validate the number of tickets per seat section
    @validates("seat_section")
    # Function to validate the number of tickets per seat section
    def limit_general_admission(self, value):
        """
        Validate the number of General Admission tickets to ensure the limit is not exceeded.
        """
        if value == VALID_SEAT_SECTIONS[0]:
            # Count the number of General Admission tickets in the database
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[0])
            # Execute the query and get the count
            count = db.session.scalar(stmt)
            # If the limit is exceeded, raise an error
            if count > 5:
                # Raise an error if the limit is exceeded
                raise ValidationError(
                    "No more General Admission tickets available, please select a different seat section"
                )

    # Validate the number of tickets per seat section
    @validates("seat_section")
    # Function to validate the number of tickets per seat section
    def limit_section_A(self, value):
        """
        Validate the number of Section A tickets to ensure the limit is not exceeded.
        """
        if value == VALID_SEAT_SECTIONS[1]:
            # Count the number of Section A tickets in the database
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[1])
            # Execute the query and get the count
            count = db.session.scalar(stmt)
            # Raise an error if the limit is exceeded
            if count > 5:
                # Raise an error if the limit is exceeded
                raise ValidationError(
                    "No more Section A tickets available, please select a different seat section"
                )

    # Validate the number of tickets per seat section
    @validates("seat_section")
    # Function to validate the number of tickets per seat section
    def limit_section_B(self, value):
        """
        Validate the number of Section B tickets to ensure the limit is not exceeded.
        """
        if value == VALID_SEAT_SECTIONS[2]:
            # Count the number of Section B tickets in the database
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[2])
            # Execute the query and get the count
            count = db.session.scalar(stmt)
            # Raise an error if the limit is exceeded
            if count > 5:
                # Raise an error if the limit is exceeded
                raise ValidationError(
                    "No more Section B tickets available, please select a different seat section"
                )

    # Validate the number of tickets per seat section
    @validates("seat_section")
    # Function to validate the number of tickets per seat section
    def limit_section_C(self, value):
        """
        Validate the number of Section C tickets to ensure the limit is not exceeded.
        """
        if value == VALID_SEAT_SECTIONS[3]:
            # Count the number of Section C tickets in the database
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[3])
            # Execute the query and get the count
            count = db.session.scalar(stmt)
            # Raise an error if the limit is exceeded
            if count > 5:
                # Raise an error if the limit is exceeded
                raise ValidationError(
                    "No more Section C tickets available, please select a different seat section"
                )
    # Validate the number of tickets per seat section
    @validates("seat_section")
    # Function to validate the number of tickets per seat section
    def limit_vip(self, value):
        """
        Validate the number of VIP tickets to ensure the limit is not exceeded.
        """
        if value == VALID_SEAT_SECTIONS[4]:
            # Count the number of VIP tickets in the database
            stmt = db.select(db.func.count()).select_from(Attending).filter_by(seat_section=VALID_SEAT_SECTIONS[4])
            # Execute the query and get the count
            count = db.session.scalar(stmt)
            # Raise an error if the limit is exceeded
            if count > 2:
                # Raise an error if the limit is exceeded
                raise ValidationError(
                    "No more VIP tickets available, please select a different seat section"
                )

    # Meta class to specify which fields to include in the serialised output
    class Meta:
        fields = (
            "id",              # The unique identifier for the attending record
            "total_tickets",   # The total number of tickets associated with this record
            "seat_section",    # The section where the seat is located
            "timestamp",       # The timestamp of when the record was created or modified
            "event_id",        # The ID of the associated event
            "attending_id",    # The ID of the associated user
            "user",            # The nested User object with selected fields
            "event",           # The nested Event object with selected fields
            "invoice"          # The nested Invoice object with selected fields
        )

# Instantiate a schema for a single Attending object
attending_schema = AttendingSchema()
# Instantiate a schema for multiple Attending objects
attendings_schema = AttendingSchema(many=True)