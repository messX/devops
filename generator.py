import time

from prometheus_client import Counter, Gauge

from nginx_report_generator import NginxReporter


class Generator:
    '''This class keeps a watch on log file
    and update stats as soon as it detect any change in the log file'''
    def __init__(self, log_file):
        self.log_file = log_file
        self.stats = {
            "total_requests_count": Counter('total_request_count', 'Total requests count'),
            "failed_requests_count": Counter('failed_request_count', 'Failed requests count'),
            "total_requests_count_by_service": Counter('total_request_count_by_service', 'Total requests count by service',
                                            ['service']),
            "total_requests_failed_count_by_service": Counter('total_request_failed_count_by_service',
                                                       'Total failed requests count by service',
                                                       ['service']),
            "total_processing_time": Counter('avg_processing_time', 'avg time to process'),
            "total_processing_time_by_url": Counter('avg_processing_time_bu_url', 'avg time to process by url', ['service']),
            "total_request_by_user":Counter('total_request_count_by_user', 'Total request by user type',
                                             ['user']),
            "requests_response_code_count": Counter('mt_apps_requests_response_code_count_nginx',
                                           'Requests count by response code', ['service', 'success_code'])
        }

    def watch_file(self):
        '''watcher to detect file change'''
        f = open(self.log_file, 'r')
        while True:
            line = f.readline()
            if not line:
                time.sleep(5)
            else:
                NginxReporter.update_stats(line, self.stats)

