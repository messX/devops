from prometheus_client import start_http_server

from generator import Generator


def run_server_watch_file():
    _file = '/home/ubuntu/logs/access.log'
    # Start up the server to expose the metrics.
    start_http_server(8080)
    print('server started at  locahost:8080')
    Generator(_file).watch_file()


if __name__ == '__main__':
    run_server_watch_file()
