import time
import traceback

from prometheus_client import Counter

from nginx_report_generator import NginxReporter


class Generator:
    """This class keeps a watch on log file
    and update stats as soon as it detect any change in the log file"""
    def __init__(self, log_file):
        self.log_file = log_file
        self.stats = {
            "total_requests_count": Counter('mt_apps_nginx_total_request_count', 'Total requests count'),
            "failed_requests_count": Counter('mt_apps_nginx_failed_request_count', 'Failed requests count'),
            "total_requests_count_by_service": Counter('mt_apps_nginx_total_request_count_by_service',
                                                       'Total requests count by service', ['service']),
            "total_requests_failed_count_by_service": Counter('mt_apps_nginx_total_request_failed_count_by_service',
                                                              'Total failed requests count by service', ['service']),
            "total_processing_time": Counter('mt_apps_nginx_total_processing_time', 'avg time to process'),
            "total_processing_time_by_url": Counter('mt_apps_nginx_total_processing_time_by_url',
                                                    'avg time to process by url', ['service']),
            "total_request_by_user": Counter('mt_apps_nginx_total_request_count_by_user', 'Total request by user type',
                                            ['user']),
            "requests_response_code_count": Counter('mt_apps_nginx_response_code_count_nginx',
                                                    'Requests count by response code', ['service', 'status'])
        }

    def watch_file(self):
        """watcher to detect file change"""
        f = open(self.log_file, 'r')
        while True:
            line = f.readline()
            if not line:
                time.sleep(5)
            else:
                try:
                    NginxReporter().update_stats(line, self.stats)
                except Exception as err:
                    traceback.print_tb(err.__traceback__)



