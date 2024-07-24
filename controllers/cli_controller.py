# Command Line Interface controllers
# seperate file follows seperation of concerns (SoC)

# Built-in Python Libraries
from datetime import datetime, date
import click

# External Libraries
from flask import Blueprint

# Imports from local files
from init import db, bcrypt
from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.event import Event
from models.attending import Attending
from models.invoice import Invoice

# blueprint is a built-in class provided by flask
# define the blueprint named "db" 
db_commands = Blueprint("db", __name__)

# cli to create the tables in the db
@db_commands.cli.command("create") 
# define the function to create the tables
def create_tables():
    # create all the tables in the db
    db.create_all()
    # print message to confirm tables were created
    print("Tables created")

# cli to drop all the tables in the db
@db_commands.cli.command("drop") 
# define the function to drop the tables
def drop_tables():
    # drop all the tables in the db
    db.drop_all()
    # print message to confirm tables were dropped
    print("Tables dropped")

# cli to count all tickets sold to an event
# to call this cli command please write 'flask db total_count <int:event_id>' 
# for example, 'flask db total_count 2' for event with id 2
@db_commands.cli.command("total_count")
@click.argument("event_id", type=int)
# define the function to count all tickets sold to an event
def count_attending(event_id):
    try:
        # Query to sum total_tickets for the specified event_id
        total_tickets_sold = db.session.query(db.func.sum(Attending.total_tickets)).filter_by(event_id=event_id).scalar()
        # if total_tickets_sold is None, set it to 0
        if total_tickets_sold is None:
            # set total_tickets_sold to 0
            total_tickets_sold = 0
        # Query to get the event with the specified event_id
        stmt = db.select(Event).filter_by(id=event_id)
        # fetch the event from the DB with correct id
        event = db.session.scalar(stmt)
        click.echo(f"Total tickets sold for Event ID {event_id}: {total_tickets_sold}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

# cli to seed all the tables in the db
@db_commands.cli.command("seed") 
# define the function to seed the tables
def seed_tables():
    # create a list of user instances including one admin user
    # that will be added to the users table
    users = [
        User(
            name="Admin",
            user_name="Admina",
            email="admin@email.com",
            # hash the password using bcrypt
            password=bcrypt.generate_password_hash("Abc12345").decode("utf-8"),
            # One admin user to test admin functionality
            is_admin=True
        ),
        User(
            name="Tom Martin",
            user_name="Tommy",
            email="tom@email.com",
            # hash the password using bcrypt
            password=bcrypt.generate_password_hash("Abc12345").decode("utf-8")
        )
    ]


    # add users to session
    db.session.add_all(users)

    # create post data to seed tables for testing
    # create a list of post instances that will be added to the posts table
    posts = [
        Post(
            title = "post 1",
            content = "this is post 1",
            date = date.today(),
            location = "Adelaide",
            user = users[0] # user_id 1, users index 0
        ),
        Post(
            title = "post 2",
            content = "this is post 2",
            date = date.today(),
            location = "Sydney",
            user = users[1] # user_id 2, users index 1
            # user_id = users[0].id
        )
    ]

    # add posts to session
    db.session.add_all(posts)

    # create comment data to seed tables for testing
    # create a list of comment instances that will be added to the comments table
    comments = [
        # Create instance of the Comment model
        Comment (
            content = "comment 1",
            timestamp = datetime.now(),
            user = users[1],
            post = posts[0]
        ),
        Comment (
            content = "comment 2",
            timestamp = datetime.now(),
            user = users[0],
            post = posts[1]
        ),
        Comment (
            content = "comment 3",
            timestamp = datetime.now(),
            user = users[1],
            post = posts[1]
        )
    ]
    # add comments to session
    db.session.add_all(comments)

    # create like data to seed tables for testing
    # create a list of like instances that will be added to the likes table
    likes = [
        # Create instance of the Comment model
        Like(
            user = users[1],
            post = posts[0]
        ),
        Like(
            user = users[0],
            post = posts[1]
        )
    ]
    # add likes to session
    db.session.add_all(likes)
 
    # create event data to seed tables for testing
    # create a list of event instances that will be added to the events table
    events = [
        Event(
            title = "Event 1",
            description = "This is event 1",
            date = "01/02/2024",
            event_admin_id = 1,
            user = users[0]
        ),
        Event(
            title = "Event 2",
            description = "This is event 2",
            date = "01/02/2024",
            event_admin_id = 2,
            user = users[1]
    )]
    # add events to session
    db.session.add_all(events)

    # create attending data to seed tables for testing
    # create a list of attending instances that will be added to the attending table
    attending = [
        Attending(
            total_tickets = 2,
            timestamp = datetime.now(),
            event_id = 1,
            attending_id = 1
        ),
        Attending(
            total_tickets = 2,
            timestamp = datetime.now(),
            event_id = 2,
            attending_id = 2
        )
    ]
    # add attending to session
    db.session.add_all(attending)

    # create invoice data to seed tables for testing
    # create a list of invoice instances that will be added to the invoice table
    invoice = [
        Invoice(
            total_cost = 12.00,
            event_id = 1,
            timestamp = datetime.now(),
            attendee_id = 1
        ),
        Invoice(
            total_cost = 12.00,
            event_id = 2,
            timestamp = datetime.now(),
            attendee_id = 2
        )
    ]
    # add invoice to session
    db.session.add_all(invoice)

    # commit all seeded data to session
    db.session.commit()
    
    # print tables seeded so we know the tables were seeded correctly
    print("Tables seeded")