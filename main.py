# Create the app

# Built-in Python Libraries
import os

# External Libraries
from flask import Flask
from marshmallow.exceptions import ValidationError

# Imports from local files
from init import db, ma, bcrypt, jwt

# Application factories, can create multiple instances of the app
# for reasons such as testing or running multiple versions of the app


def create_app():
    app = Flask(__name__)

    # Telling flask to not sort using their own config, return what
    # you get from marshmallow
    app.json.sort_keys = False
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

    # Error handling
    # If a validation error occurs, return the error message and status code
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400

    # Register blueprints into the main app instance so we can use their
    # different entities using the 'register_blueprint' method
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    # Import the blueprints
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.post_controller import posts_bp
    app.register_blueprint(posts_bp)

    from controllers.event_controller import events_bp
    app.register_blueprint(events_bp)

    from controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    # Return the instance of the flask app
    return app
