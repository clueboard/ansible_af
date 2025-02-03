from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .flask_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///af.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(256), unique=True, nullable=False)
    macaddr = db.Column(db.String(17), unique=True, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    registration_complete = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Hosts('{self.id}', '{self.ip}', '{self.macaddr}', '{self.registered_at}', '{self.registration_complete}')"  # noqa


def upsert_host(ip):
    existing_host = Hosts.query.filter_by(ip=ip).first()

    if existing_host:
        existing_host.registered_at = datetime.utcnow()
        existing_host.registration_complete = False
        db.session.commit()
        app.logger.info("Updated record for %s", ip)

    else:
        new_host = Hosts(ip=ip)
        db.session.add(new_host)
        db.session.commit()
        app.logger.info("Created record for %s", ip)


# Create the database tables
with app.app_context():
    db.create_all()
