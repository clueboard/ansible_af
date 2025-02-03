from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment
template_dir = '/etc/ansible/playbooks/templates'
jinja2 = Environment(loader=FileSystemLoader(template_dir))


def render_template(template_name, context):
    template = jinja2.get_template(template_name)
    return template.render(context)
