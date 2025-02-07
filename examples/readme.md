# Ansible AF Example Files

This directory contains a number of example files you can use to get started with Ansible AF. You will need to customize them for your environment.

* [etc_ansible_hosts](etc_ansible_hosts): Ansible host registry to be installed into `/etc/ansible/hosts`
* [etc-ansible-playbooks-ansible_af.yaml](etc-ansible-playbooks-ansible_af.yaml): Anisble playbook for installing ansible_af. Use in place or install to `/etc/ansible/playbooks/ansible-af.yaml`.
* [etc-ansible-playbooks-ansible_af-upgrade.yaml](etc-ansible-playbooks-ansible_af-upgrade.yaml): Anisble playbook for upgrading ansible_af to the latest version from git. Use in place or install to `/etc/ansible/playbooks/ansible-af.yaml`.
* [etc_ansible_playbooks_configure_netplan_knode.yaml](etc_ansible_playbooks_configure_netplan_knode.yaml): Configure netplan playbook for the knodes, install as `/etc/ansible/playbooks/configure_netplan_knode.yaml`
* [etc_ansible_playbooks_templates_netplan_knode.yaml.j2](etc_ansible_playbooks_templates_netplan_knode.yaml.j2): Jinja2 template for the netplan configuration, install as `/etc/ansible/playbooks/templates/netplan_knode.yaml.j2`
* [etc_ansible_playbooks_templates_armbian_first_boot.j2](etc_ansible_playbooks_templates_armbian_first_boot.j2): Jinja2 template for the armbian_first_boot file, install as `/etc/ansible/playbooks/templates/armbian_first_boot.j2`
