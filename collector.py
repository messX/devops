import os

from generator import Generator
from prometheus_client import start_http_server


def run_server_watch_file():
    """
    Start up the server to expose the metrics.
    """
    _file = '/mnt/logs/access.log'
    start_http_server(8080)
    print('server started at  localhost:8080')
    Generator(_file).watch_file()


if __name__ == '__main__':
    run_server_watch_file()
