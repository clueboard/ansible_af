from .flask_app import app
from .db import db
from . import routes  # noqa

# Create the database tables
with app.app_context():
    db.create_all()
