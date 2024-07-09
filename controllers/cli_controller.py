# Command Line Interface controllers
# Having these in a seperate file follows seperation 
# of concern 

from flask import Blueprint

from init import db, bcrypt
from models.user import User

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
    # commit users to session
    db.session.commit()

    print("Tables seeded")