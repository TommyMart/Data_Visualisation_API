# External Libraries
# Flask SQLAlchemy, Marshmallow, Bcrypt, JWTManager
# These libraries will be used in the main.py file
# to initialise the app instance
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create instances of the libraries
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
