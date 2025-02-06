from os import environ

ansible_path = environ.get('ANSIBLE_PATH', '/etc/ansible')
inventory_path = environ.get('ANSIBLE_INVENTORY_PATH', ansible_path + '/hosts')
playbook_path = environ.get('ANSIBLE_PLAYBOOK_PATH', ansible_path + '/playbooks')
template_dir = environ.get('ANSIBLE_AF_TEMPLATE_DIR', playbook_path + '/templates')
allow_dynamic_hosts = environ.get('ANSIBLE_AF_ALLOW_DYNAMIC_HOSTS') in ["True", "true", "1"]
allowlist = environ.get('ANSIBLE_AF_ALLOWLIST', 'armbian_first_boot').split(',')
denylist = environ.get('ANSIBLE_AF_DENYLIST', '').split(',')
