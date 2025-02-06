from datetime import datetime, timedelta
from time import sleep

from milc import cli

from .flask_app import app
from .config import host_prep_wait_time, inventory_path, playbook_path
from .db import db, Hosts


@cli.argument('--loop', action='store_boolean', help='running in an infinite loop.')
@cli.entrypoint("Process the ansible af queue")
def main(cli):
    with app.app_context():
        while True:
            host = Hosts.query.filter(
                Hosts.registered_at.isnot(None),
                Hosts.playbook_complete.isnot(True),
                Hosts.registered_at < datetime.utcnow() - timedelta(seconds=host_prep_wait_time),
            ).order_by(Hosts.registered_at.asc()).first()

            if host:
                app.logger.info('Running playbook %s against host: %s', host.playbook, host)
                full_playbook_path = f'{playbook_path}/{host.playbook}.yaml'
                playbook_args = (
                    'ansible-playbook',
                    '-i', inventory_path,
                    '-l', host.hostname,
                    full_playbook_path,
                )
                playbook_result = cli.run(playbook_args, capture_output=False)

                if playbook_result.returncode == 0:
                    # Mark the host as complete
                    host.playbook_complete = True

                    db.session.commit()
                    app.logger.info("Marked %s as completed", host)

            if not cli.args.loop:
                break

            sleep(1)


if __name__ == "__main__":
    cli()
