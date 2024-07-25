# External Libraries
from marshmallow import fields, validates
from marshmallow.validate import OneOf
from marshmallow.exceptions import ValidationError

# Imports from local files
from init import db, ma
from models.user import User

# Constants
# Define valid seat sections
VALID_SEAT_SECTIONS = ("General Admission", "Section A",
                       "Section B", "Section C", "VIP")

# Define the maximum number of tickets per user per event
MAX_TICKETS_PER_USER = 5
# Define the maximum number of tickets per email address (commented out for now)
# MAX_TICKETS_PER_EMAIL = 5

# Attending model class


class Attending(db.Model):
    # Define the table name
    __tablename__ = "attending"

    # Table Attributes
    # Unique identifier for each attending record, serves as the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Total number of tickets associated with this attending record, default is 1
    total_tickets = db.Column(db.Integer, default=1)
    # Section where the seat is located, default is "General Admission"
    seat_section = db.Column(db.String, default="General Admission")
    # Date when the attending record was created or modified
    timestamp = db.Column(db.Date)

    # Foreign Keys
    # Foreign key to the 'events' table, indicating which event this record 
    # is associated with
    event_id = db.Column(db.Integer, db.ForeignKey(
        "events.id"), nullable=False)
    # Foreign key to the 'users' table, indicating which user this record is 
    # associated with
    attending_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    # Establish a relationship to the User model, allowing access to the user 
    # attending the event
    user = db.relationship("User", back_populates="attending")
    # Establish a relationship to the Event model, allowing access to the event details
    event = db.relationship("Event", back_populates="attending")
    # Establish a relationship to the Invoice model, allowing access to invoices 
    # related to this record
    # Cascade delete ensures related invoices are removed when this record is deleted
    invoice = db.relationship(
        "Invoice", back_populates="attending", cascade="all, delete")

# Schema for serializing and deserializing Attending objects


class AttendingSchema(ma.Schema):
    try:
        # Nested schema for User model, including limited fields
        user = fields.Nested("UserSchema", only=["name", "email", "is_admin"])
        # Nested schema for Event model, including limited fields
        event = fields.Nested("EventSchema", only=["title", "ticket_price"])
        # Nested schema for Invoice model, including limited fields
        invoice = fields.Nested("InvoiceSchema", only=["total_cost"])

        # Validate seat_section against predefined valid sections
        seat_section = fields.String(
            # Ensure value is one of the predefined valid sections
            validate=OneOf(VALID_SEAT_SECTIONS),
            # Error message if value is not valid
            error="Please enter a valid seating section"
        )

        # Validate total_tickets to ensure it does not exceed the maximum 
        # allowed per user per event
        @validates("total_tickets")
        def validate_max_tickets(self, value):
            """
            Validate the total number of tickets to ensure it does not exceed the maximum 
            allowed per user per event.
            """
            if value > MAX_TICKETS_PER_USER:
                raise ValidationError(
                    f"Maximum {
                        MAX_TICKETS_PER_USER} tickets allowed per user per event"
                )
            if value < 1:
                # Ensure the number of tickets is at least 1
                raise ValidationError("Please enter a valid number of tickets")

        # Function to validate the number of tickets per seat section
        @validates("seat_section")
        def limit_general_admission(self, value):
            """
            Validate the number of General Admission tickets to ensure the limit is not exceeded.
            """
            if value == VALID_SEAT_SECTIONS[0]:
                count = db.session.scalar(
                    db.select(db.func.count()).select_from(Attending).filter_by(
                        seat_section=VALID_SEAT_SECTIONS[0])
                )
                if count > 5:
                    raise ValidationError(
                        "No more General Admission tickets available, please select a different seat section"
                    )

        @validates("seat_section")
        def limit_section_A(self, value):
            """
            Validate the number of Section A tickets to ensure the limit is not exceeded.
            """
            if value == VALID_SEAT_SECTIONS[1]:
                count = db.session.scalar(
                    db.select(db.func.count()).select_from(Attending).filter_by(
                        seat_section=VALID_SEAT_SECTIONS[1])
                )
                if count > 5:
                    raise ValidationError(
                        "No more Section A tickets available, please select a different seat section"
                    )

        @validates("seat_section")
        def limit_section_B(self, value):
            """
            Validate the number of Section B tickets to ensure the limit is not exceeded.
            """
            if value == VALID_SEAT_SECTIONS[2]:
                count = db.session.scalar(
                    db.select(db.func.count()).select_from(Attending).filter_by(
                        seat_section=VALID_SEAT_SECTIONS[2])
                )
                if count > 5:
                    raise ValidationError(
                        "No more Section B tickets available, please select a different seat section"
                    )

        @validates("seat_section")
        def limit_section_C(self, value):
            """
            Validate the number of Section C tickets to ensure the limit is not exceeded.
            """
            if value == VALID_SEAT_SECTIONS[3]:
                count = db.session.scalar(
                    db.select(db.func.count()).select_from(Attending).filter_by(
                        seat_section=VALID_SEAT_SECTIONS[3])
                )
                if count > 5:
                    raise ValidationError(
                        "No more Section C tickets available, please select a different seat section"
                    )

        @validates("seat_section")
        def limit_vip(self, value):
            """
            Validate the number of VIP tickets to ensure the limit is not exceeded.
            """
            if value == VALID_SEAT_SECTIONS[4]:
                count = db.session.scalar(
                    db.select(db.func.count()).select_from(Attending).filter_by(
                        seat_section=VALID_SEAT_SECTIONS[4])
                )
                if count > 2:
                    raise ValidationError(
                        "No more VIP tickets available, please select a different seat section"
                    )

        # Meta class to specify which fields to include in the serialized output
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
    except Exception as e:
        # Handle unexpected errors
        print(str(e)), 500


# Instantiate a schema for a single Attending object
attending_schema = AttendingSchema()
# Instantiate a schema for multiple Attending objects
attendings_schema = AttendingSchema(many=True)
