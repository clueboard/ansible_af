from datetime import datetime, timedelta
from time import sleep

from milc import cli

from .flask_app import app
from .config import host_prep_wait_time, inventory_path, playbook_path, ssh_username
from .db import db, Hosts


@cli.argument('--loop', action='store_boolean', help='running in an infinite loop.')
@cli.entrypoint('Process the ansible af queue')
def main(cli):
    with app.app_context():
        while True:
            host = Hosts.query.filter(
                Hosts.registered_at.isnot(None),
                Hosts.playbook_complete.isnot(True),
                Hosts.registered_at < datetime.utcnow() - timedelta(seconds=host_prep_wait_time),
            ).order_by(Hosts.registered_at.asc()).first()

            if host:
                cli.log.info('Running playbook %s against host: %s', host.playbook, host)

                # Increment the attempt count
                host.playbook_attempts += 1
                db.session.commit()

                # Run the playbook
                full_playbook_path = f'{playbook_path}/{host.playbook}.yaml'
                playbook_args = [
                    'ansible-playbook',
                    '-i',
                    inventory_path,
                    '-l',
                    host.hostname,
                ]

                if ssh_username:
                    playbook_args.extend(['-u', ssh_username])

                playbook_args.append(full_playbook_path)

                playbook_result = cli.run(playbook_args, capture_output=False)

                if playbook_result.returncode == 0:
                    # Mark the host as complete
                    host.playbook_complete = True

                    db.session.commit()
                    cli.log.info('Marked %s as completed', host)

                elif host.playbook_attempts > 2:
                    cli.log.info('Too many errors for %s, marking as completed!', host)
                    host.playbook_complete = True

                else:
                    cli.log.info(
                        'Encountered error on host %s for playbook %s, waiting %s seconds...',
                        host.hostname,
                        host.playbook,
                        host_prep_wait_time
                    )
                    host.registered_at = datetime.utcnow()

            if not cli.args.loop:
                break

            sleep(1)


if __name__ == '__main__':
    cli()
