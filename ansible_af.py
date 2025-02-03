import os
from datetime import datetime
from threading import Thread
from time import sleep

from flask import Flask, abort, request, send_file
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader

from inventory import find_host_by_ip


# App configuration
config = {
    'template_dir': '/etc/ansible/playbooks/templates',
    'allow_dynamic_hosts': False,

    # Specify what files are allowed to be rendered, or denied.
    # If either of these are non-empty then only specifically allowed files will be rendered
    'allowlist': ['armbian_first_boot'],
    'denylist': [],
}

# Instaniate the application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///af.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jinja2 = Environment(loader=FileSystemLoader(config['template_dir']))


# DB Model
class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(256), unique=True, nullable=False)
    macaddr = db.Column(db.String(17), unique=True, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    registration_complete = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Hosts('{self.id}', '{self.ip}', '{self.macaddr}', '{self.registered_at}', '{self.registration_complete}')"


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


# Background thread section
def playbook_runner():
    """Background thread that kicks off playbooks after a machine registers itself.
    """
    with app.app_context():
        while True:
            host = Hosts.query.filter(
                Hosts.registered_at.isnot(None),
                Hosts.registration_complete == False,
            ).order_by(Hosts.registered_at.asc()).first()

            if host:
                app.logger.info('Would run against host: %s', host)
                host.registration_complete = True
                db.session.commit()
                app.logger.info("Updated record for %s", host)

            app.logger.info('loop')
            sleep(60)

Thread(target=playbook_runner, daemon=True).start()


# Helper functions
def render_template(template_name, context):
    template = jinja2.get_template(template_name + '.j2')

    return template.render(context)


def is_render_permitted(filename):
    if not config['allowlist'] and not config['denylist']:
        return True

    if filename in config['denylist']:
        return False

    if filename in config['allowlist']:
        return True

    return False


@app.route("/")
def home():
    return "Helo, World!"


@app.route("/register/<host_template>")
def register_first_boot(host_template):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    host = find_host_by_ip(client_ip)
    filename = os.path.basename(host_template)  # Ensure they don't try to read other files with ../
    full_path = os.path.join(config['template_dir'], filename) + '.j2'

    # Validate the request
    if not is_render_permitted(filename):
        app.logger.error('Request for unpermitted file: %s', filename)
        abort(403)

    if not os.path.exists(full_path):
        app.logger.error("Request for template that doesn't exist: %s", filename)
        abort(404)

    # Deliver the template
    if host:
        upsert_host(client_ip)

        return render_template(filename, host)

    if config['allow_dynamic_hosts']:
        pass

    app.logger.error("Request from IP that's not in our inventory: %s", client_ip)
    abort(404)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
