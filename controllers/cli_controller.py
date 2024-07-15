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
def create_tables():
    db.create_all()
    print("Tables created")

# cli to drop all the tables in the db
@db_commands.cli.command("drop") 
def drop_tables():
    db.drop_all()
    print("Tables dropped")

# cli to count all tickets sold to an event
# to call this cli command please write 'flask db total_count <int:event_id>' 
# for example, 'flask db total_count 2' for event with id 2
@db_commands.cli.command("total_count")
@click.argument("event_id", type=int)
def count_attending(event_id):
    try:
        # Query to sum total_tickets for the specified event_id
        total_tickets_sold = db.session.query(db.func.sum(Attending.total_tickets)).filter_by(event_id=event_id).scalar()
        
        if total_tickets_sold is None:
            total_tickets_sold = 0
        
        click.echo(f"Total tickets sold for Event ID {event_id}: {total_tickets_sold}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

# cli to seed all the tables in the db
@db_commands.cli.command("seed") 
def seed_tables():
    # create a list of user instances including one admin user
    users = [
        User(
            email="admin@email.com",
            # hash the password using bcrypt, 
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="Tom Martin",
            email="tom@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]


    # add users to session
    db.session.add_all(users)

    # create post data to seed tables for testing
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

    db.session.add_all(comments)

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

    db.session.add_all(likes)

    events = [
        Event(
            title = "Event 1",
            description = "This is event 1",
            date = "01/02/2024",
            event_admin_id = 2,
            user = users[1]
        )
    ]

    db.session.add_all(events)

    attending = [
        Attending(
            total_tickets = 2,
            timestamp = datetime.now(),
            event_id = 1,
            attending_id = 1
        )
    ]

    db.session.add_all(attending)

    invoice = [
        Invoice(
            total_cost = 12.00,
            event_id = 1,
            timestamp = datetime.now(),
            attendee_id = 1
        )
    ]

    db.session.add_all(invoice)

    # commit all seeded data to session
    db.session.commit()
    
    # print tables seeded so we know the tables were seeded correctly
    print("Tables seeded")