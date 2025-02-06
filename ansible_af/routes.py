import os
from flask import abort, request
from jinja2 import Environment, FileSystemLoader

from .config import allowlist, denylist, inventory_path, template_dir
from .db import get_random_row, upsert_host
from .flask_app import app
from .inventory import find_host_by_ip

# Instaniate the application
jinja2 = Environment(loader=FileSystemLoader(template_dir))


# Helper functions
def render_template(template_name, context):
    """Render a jinja2 template from the template_dir path.

    context is a dictionary of values that will be available inside the template.
    """
    template = jinja2.get_template(template_name + '.j2')

    return template.render(context)


def is_render_permitted(filename):
    if not allowlist and not denylist:
        return True

    if filename in denylist:
        return False

    if filename in allowlist:
        return True

    return False


@app.route("/")
def home():
    return "https://github.com/clueboard/ansible_af"


@app.route("/readiness_probe")
def readiness_probe():
    if not os.path.exists(inventory_path):
        app.logger.error("Ansible inventory not found!")
        abort(500)

    if not os.path.exists(template_dir):
        app.logger.error("Ansible template directory not found!")
        abort(500)

    get_random_row()

    return "Ready to serve!"


@app.route("/register/<playbook>")
def register_first_boot(playbook):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    host = find_host_by_ip(client_ip)
    filename = os.path.basename(playbook)  # Ensure they don't try to read other files with ../
    full_path = os.path.join(template_dir, filename) + '.j2'

    # Validate the request
    if not is_render_permitted(filename):
        app.logger.error('Request for unpermitted file: %s', filename)
        abort(403)

    if not os.path.exists(full_path):
        app.logger.error("Request for template that doesn't exist: %s", filename)
        abort(404)

    # Deliver the template
    if host:
        upsert_host(client_ip, playbook=playbook, hostname=host['inventory_hostname'], register=True)

        return render_template(filename, host)

    # If they get here they weren't in our Ansible inventory
    app.logger.error("Request from IP that's not in our inventory: %s", client_ip)
    abort(404)
