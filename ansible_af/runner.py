from time import sleep

from milc import cli

from .flask_app import app
from .config import inventory_path, playbook_path
from .db import db, Hosts


@cli.argument('--loop', action='store_boolean', help='running in an infinite loop.')
@cli.entrypoint("Process the ansible af queue")
def main(cli):
    with app.app_context():
        while True:
            host = Hosts.query.filter(
                Hosts.registered_at.isnot(None),
                Hosts.playbook_complete.isnot(True),
            ).order_by(Hosts.registered_at.asc()).first()

            if host:
                app.logger.info('Running playbook %s against host: %s', host.playbook, host)
                full_playbook_path = playbook_path + '/' + host.playbook + '.yml'
                playbook_args = (
                    'ansible-playbook',
                    '-i', inventory_path,
                    '-l', host.hostname,
                    '/etc/ansible/playbooks/armbian_first_boot.yaml',
                )

                cli.run(playbook_args, capture_output=False)

                # Mark the host as complete
                host.playbook_complete = True

                db.session.commit()
                app.logger.info("Marked %s as completed", host)

            if not cli.args.loop:
                break

            app.logger.info('loop')
            sleep(60)


if __name__ == "__main__":
    cli()
