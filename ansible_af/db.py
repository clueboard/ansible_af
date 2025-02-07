from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .flask_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///af.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(256), unique=True, nullable=False)
    hostname = db.Column(db.String(256), unique=True, nullable=True)
    macaddr = db.Column(db.String(17), unique=True, nullable=True)
    playbook = db.Column(db.String(256), nullable=True)
    registered_at = db.Column(db.DateTime, nullable=True)
    playbook_attempts = db.Column(db.Integer, nullable=False, default=0)
    playbook_complete = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return (
            f"Hosts(id='{self.id}', ip='{self.ip}', hostname='{self.hostname}', macaddr='{self.macaddr}', "
            f"playbook='{self.playbook}', registered_at='{self.registered_at}', playbook_attempts='{self.playbook_attempts}', "
            f"playbook_complete='{self.playbook_complete}')"
        )


def get_random_row():
    """Fetches a single row. Despite the name, entropy of this function is very low.
    """
    return Hosts.query.limit(1).first()


def upsert_host(ip, macaddr=None, hostname=None, playbook=None, register=False):
    """Add or update a host.
    """
    existing_host = Hosts.query.filter_by(ip=ip).first()

    if existing_host:
        existing_host.registered_at = datetime.utcnow() if register else None
        existing_host.playbook_attempts = 0
        existing_host.playbook_complete = False

        if macaddr:
            existing_host.macaddr = macaddr

        if playbook:
            existing_host.playbook = playbook

        if hostname:
            existing_host.hostname = hostname

        db.session.commit()
        app.logger.info('Updated record for %s: %s', ip, existing_host)

    else:
        new_host = Hosts(ip=ip, macaddr=macaddr, playbook=playbook, hostname=hostname)
        new_host.registered_at = datetime.utcnow() if register else None

        db.session.add(new_host)
        db.session.commit()
        app.logger.info('Created record for %s: %s', ip, new_host)


# Create the database tables
with app.app_context():
    db.create_all()
