import pytest
from unittest.mock import patch
from ansible_af.flask_app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'https://github.com/clueboard/ansible_af' in rv.data


def test_readiness_probe(client):
    with patch('ansible_af.routes.os.path.exists') as mock_exists, \
         patch('ansible_af.routes.get_random_row'):
        mock_exists.side_effect = lambda path: True

        rv = client.get('/readiness_probe')
        assert rv.status_code == 200
        assert b'Ready to serve!\n' in rv.data


def test_register_first_boot(client):
    with patch('ansible_af.routes.find_host_by_ip') as mock_find_host_by_ip, \
         patch('ansible_af.routes.is_render_permitted') as mock_is_render_permitted, \
         patch('ansible_af.routes.os.path.exists') as mock_exists, \
         patch('ansible_af.routes.render_template') as mock_render_template, \
         patch('ansible_af.routes.upsert_host') as mock_upsert_host:

        mock_find_host_by_ip.return_value = {'inventory_hostname': 'test_host'}
        mock_is_render_permitted.return_value = True
        mock_exists.side_effect = lambda path: True
        mock_render_template.return_value = 'Rendered Template'
        assert mock_upsert_host

        rv = client.get('/register/test_playbook')
        assert rv.status_code == 200
        assert b'Rendered Template' in rv.data

        mock_find_host_by_ip.return_value = None
        rv = client.get('/register/test_playbook')
        assert rv.status_code == 404
