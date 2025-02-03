from time import sleep

from milc import cli

from .flask_app import app
from .db import db, Hosts


@cli.entrypoint("Process the ansible af queue")
def main(cli):
    with app.app_context():
        while True:
            host = Hosts.query.filter(
                Hosts.registered_at.isnot(None),
                Hosts.registration_complete.isnot(True),
            ).order_by(Hosts.registered_at.asc()).first()

            if host:
                app.logger.info('Would run against host: %s', host)
                host.registration_complete = True
                db.session.commit()
                app.logger.info("Updated record for %s", host)

            app.logger.info('loop')
            sleep(60)


if __name__ == "__main__":
    cli()
