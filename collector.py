import os

from generator import Generator
from prometheus_client import start_http_server


def run_server_watch_file():
    """
    Start up the server to expose the metrics.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    log_dir = '{}/logs'.format(dir_path)
    files = [file for file in os.listdir(log_dir) if file.endswith('.log')]
    _file = '{}/{}'.format(log_dir, files[0])
    start_http_server(8080)
    print('server started at  localhost:8080')
    Generator(_file).watch_file()


if __name__ == '__main__':
    run_server_watch_file()
