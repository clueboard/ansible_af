import os
from flask import abort, request
from jinja2 import Environment, FileSystemLoader

from .config import allow_dynamic_hosts, allowlist, denylist, template_dir
from .db import upsert_host
from .flask_app import app
from .inventory import find_host_by_ip


jinja2 = Environment(loader=FileSystemLoader(template_dir))


# Helper functions
def render_template(template_name, context):
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
    return "Helo, World!"


@app.route("/register/<host_template>")
def register_first_boot(host_template):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    host = find_host_by_ip(client_ip)
    filename = os.path.basename(host_template)  # Ensure they don't try to read other files with ../
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
        upsert_host(client_ip)

        return render_template(filename, host)

    if allow_dynamic_hosts:
        pass

    app.logger.error("Request from IP that's not in our inventory: %s", client_ip)
    abort(404)
