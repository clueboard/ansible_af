from os import environ

ansible_path = environ.get('ANSIBLE_PATH', '/etc/ansible')
inventory_path = environ.get('ANSIBLE_INVENTORY_PATH', ansible_path + '/hosts')
playbook_path = environ.get('ANSIBLE_PLAYBOOK_PATH', ansible_path + '/playbooks')
template_dir = environ.get('ANSIBLE_AF_TEMPLATE_DIR', playbook_path + '/templates')
allowlist = environ.get('ANSIBLE_AF_ALLOWLIST', 'armbian_first_boot*').split(',')
denylist = environ.get('ANSIBLE_AF_DENYLIST', '').split(',')
host_prep_wait_time = int(environ.get('ANSIBLE_AF_HOST_WAIT', '30'))
host_ip_key = environ.get('ANSIBLE_AF_HOST_IP_KEY', 'cluster_ip')
