from os import environ

template_dir = environ.get('ANSIBLE_AF_TEMPLATE_DIR', '/etc/ansible/playbooks/templates')
allow_dynamic_hosts = environ.get('ANSIBLE_AF_ALLOW_DYNAMIC_HOSTS') in ["True", "true", "1"]
allowlist = environ.get('ANSIBLE_AF_ALLOWLIST', 'armbian_first_boot').split(',')
denylist = environ.get('ANSIBLE_AF_DENYLIST', '').split(',')
