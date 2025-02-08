import os
import importlib
import pytest

import ansible_af.config


def test_ansible_path(monkeypatch):
    monkeypatch.setenv('ANSIBLE_PATH', '/custom/ansible')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_PATH', raising=False)
    assert ansible_af.config.ansible_path == '/custom/ansible'
    assert ansible_af.config.inventory_path == '/custom/ansible/hosts'
    assert ansible_af.config.playbook_path == '/custom/ansible/playbooks'
    assert ansible_af.config.template_dir == '/custom/ansible/playbooks/templates'

def test_default_ansible_path(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'
    assert ansible_af.config.template_dir == '/etc/ansible/playbooks/templates'

def test_inventory_path(monkeypatch):
    monkeypatch.setenv('ANSIBLE_INVENTORY_PATH', '/custom/inventory')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_INVENTORY_PATH', raising=False)
    assert ansible_af.config.inventory_path == '/custom/inventory'
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'
    assert ansible_af.config.template_dir == '/etc/ansible/playbooks/templates'

def test_default_inventory_path(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'
    assert ansible_af.config.template_dir == '/etc/ansible/playbooks/templates'

def test_playbook_path(monkeypatch):
    monkeypatch.setenv('ANSIBLE_PLAYBOOK_PATH', '/custom/playbooks')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_PLAYBOOK_PATH', raising=False)
    assert ansible_af.config.playbook_path == '/custom/playbooks'
    assert ansible_af.config.template_dir == '/custom/playbooks/templates'
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'

def test_default_playbook_path(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'
    assert ansible_af.config.template_dir == '/etc/ansible/playbooks/templates'

def test_template_dir(monkeypatch):
    monkeypatch.setenv('ANSIBLE_AF_TEMPLATE_DIR', '/custom/templates')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_AF_TEMPLATE_DIR', raising=False)
    assert ansible_af.config.template_dir == '/custom/templates'
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'

def test_default_template_dir(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.ansible_path == '/etc/ansible'
    assert ansible_af.config.inventory_path == '/etc/ansible/hosts'
    assert ansible_af.config.playbook_path == '/etc/ansible/playbooks'
    assert ansible_af.config.template_dir == '/etc/ansible/playbooks/templates'

def test_allowlist(monkeypatch):
    monkeypatch.setenv('ANSIBLE_AF_ALLOWLIST', 'test1,test2')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_AF_ALLOWLIST', raising=False)
    assert ansible_af.config.allowlist == ['test1', 'test2']

def test_default_allowlist(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.allowlist == ['armbian_first_boot*']

def test_denylist(monkeypatch):
    monkeypatch.setenv('ANSIBLE_AF_DENYLIST', 'test1,test2')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_AF_DENYLIST', raising=False)
    assert ansible_af.config.denylist == ['test1', 'test2']

def test_default_denylist(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.denylist == ['']

def test_host_prep_wait_time(monkeypatch):
    monkeypatch.setenv('ANSIBLE_AF_HOST_WAIT', '60')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_AF_HOST_WAIT', raising=False)
    assert ansible_af.config.host_prep_wait_time == 60

def test_default_host_prep_wait_time(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.host_prep_wait_time == 30

def test_ssh_username(monkeypatch):
    monkeypatch.setenv('ANSIBLE_AF_SSH_USERNAME', 'fred')
    importlib.reload(ansible_af.config)
    monkeypatch.delenv('ANSIBLE_AF_SSH_USERNAME', raising=False)
    assert ansible_af.config.ssh_username == 'fred'

def test_default_host_prep_wait_time(monkeypatch):
    importlib.reload(ansible_af.config)
    assert ansible_af.config.ssh_username == None
