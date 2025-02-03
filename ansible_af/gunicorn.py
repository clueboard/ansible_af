import sys

from milc import cli
import gunicorn.app.wsgiapp


@cli.argument('--worker-class', default='sync', help='The gunicorn worker class to use. Default: sync')
@cli.argument('--workers', type=int, default=4, help='The number of gunicorn workers to start. Default: 4')
@cli.argument('--port', type=int, default=5000, help='The port to listen on. Default: 5000')
@cli.argument('--listen', default='0.0.0.0', help='The IP to listen on. Default: 0.0.0.0')
@cli.entrypoint("Run ansible af using gunicorn.")
def main(cli):
    # ugly hack :(
    sys.argv = [
        "gunicorn",
        "-b", f"{cli.args.listen}:{cli.args.port}",
        "-w", str(cli.args.workers),
        "-k", str(cli.args.worker_class),
        "ansible_af:app"
    ]
    gunicorn.app.wsgiapp.run()
