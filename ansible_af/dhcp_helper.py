from milc import cli

from .flask_app import app
from .db import db, Hosts


@cli.argument('hostname', nargs='?', arg_only=True, help='Hostname for the client, if known')
@cli.argument('ip_addr', arg_only=True, help='IP Address')
@cli.argument('mac_addr', arg_only=True, help='Ethernet Hardware Mac Address')
@cli.argument('action', arg_only=True, help='add, del, old')
@cli.entrypoint("Register a DHCP host")
def main(cli):
    if cli.args.action == 'del':
        return

    with app.app_context():
        host = Hosts.query.filter(Hosts.ip == cli.args.ip_addr).first()

        if host:
            host.macaddr = cli.args.mac_addr
            host.registered_at = None

            db.session.commit()
            cli.log.info("Updated record for %s", cli.args.ip_addr)

        else:
            host = Hosts(ip=cli.args.ip_addr, macaddr=cli.args.mac_addr, registered_at=None)

            db.session.add(host)
            db.session.commit()
            cli.log.info("Added record for %s", cli.args.ip_addr)


if __name__ == "__main__":
    cli()
