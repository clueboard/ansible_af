from milc import cli

from .flask_app import app
from .db import upsert_host


@cli.argument('hostname', nargs='?', arg_only=True, help='Hostname for the client, if known')
@cli.argument('ip_addr', arg_only=True, help='IP Address')
@cli.argument('mac_addr', arg_only=True, help='Ethernet Hardware Mac Address')
@cli.argument('action', arg_only=True, help='add, del, old')
@cli.entrypoint('Register a DHCP host')
def main(cli):
    if cli.args.action == 'del':
        return

    with app.app_context():
        upsert_host(ip=cli.args.ip_addr, macaddr=cli.args.mac_addr)


if __name__ == '__main__':
    cli()
