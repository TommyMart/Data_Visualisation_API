# Create the app

import os
from flask import Flask

# Importing objects from init.py
from init import db, ma, bcrypt, jwt

# Application factories, can create multiple instances of the app
# for reasons such as testing or running multiple versions of the app

def create_app():
    app = Flask(__name__)

    # Connection string or DB URI - Universal Resource Indicator
    # Get private DB URI and JWT strings from .env file using os 
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # Secret key, JWT token 
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # Initialise with this instance of application
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Return the instance of the flask app
    return app