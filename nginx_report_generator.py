import re
from datetime import datetime


class NginxParsing:
    LOG_SPECIAL_SYMBOLS = {
        '\[': '\\[',
        '\]': '\\]',
        '\"': '\\"',
        '\|': '\\|',
    }

    LOG_PARAMS = {
        '\$body_bytes_sent': '(?P<body_bytes_sent>\d+)',
        '\$bytes_sent': '(?P<bytes_sent>\d+)',
        '\$connection': 'NOT_IMPLEMENTED',
        '\$connection_requests': '(?P<connection_requests>\d+)',
        '\$host': '(?P<host>[A-Za-z0-9-\.]+)',
        '\$http_referer': '(?P<http_referer>[\d\D]+|)',
        '\$http_user_agent': '(?P<http_user_agent>[\d\D]+|)',  # agent can be empty
        # '\$http_x_forwarded_for': '(?P<http_x_forwarded_for>[\d\D.,\-\s]+)',
        '\$http_x_forwarded_for': '(?P<http_x_forwarded_for>[\d\D]+|)',
        '\$msec': '(?P<msec>\d+)',
        '\$pipe': '(?P<pipe>[.p])',
        '\$remote_addr': '(?P<remote_addr>\d+.\d+.\d+.\d+)',
        '\$remote_user': '(?P<remote_user>[\D\d]+)',
        '\$request_length': '(?P<request_length>\d+)',
        '\$status': '(?P<status>\d+)',
        '\$time_iso8601': 'NOT_IMPLEMENTED',
        '\$time_local': '(?P<time_local>[0-3][0-9]/[A-Za-z]{3}/[0-9]{4}:[0-9]{2}:[0-5][0-9]:[0-5][0-9] [-+0-9]+)',
        '\$upstream_addr': '(?P<upstream_addr>[\-A-Za-z0-9.:, ]+)',  # ip:port and unix:socket-path
        '\$upstream_response_time': '(?P<upstream_response_time>[-.\d,: ]+)',
        '\$upstream_status': '(?P<upstream_status>[\-0-9,: ]+)',
        '\$uid_got': '(?P<uid_got>[\-0-9A-Za-z=]+)',
        '\$uid_set': '(?P<uid_set>[\-0-9A-Za-z=]+)',
        '\$abCookieValue': '(?P<ab_cookie_value>[A|B])',
        '\$request': '(?P<request_request_method>[A-Z]+) (?P<request_request_uri>[\d\D]+) '
                     '(?P<request_request_http_version>HTTP/[0-9.]+)',
        '\$req_time': '(?P<request_time>[\d.]+)',
    }

    LOG_PARAMS.update({
        '\$cookie_ab_v6_version': '(?P<cookie_ab_v6_version>(v\d|-))',
        '\$abv3_6': '(?P<abv3_6>(v\d|-))',
        '\$ab_var': '(?P<ab_var>(v\d|-))',

        '\$upstream_response_length': '(?P<upstream_response_length>.*)',  # ip:port and unix:socket-path
        '\$upstream_cache_status': '(?P<upstream_cache_status>.*)',

        '\$upstream_addr': '(?P<upstream_addr>.*)',  # ip:port and unix:socket-path
        '\$upstream_response_time': '(?P<upstream_response_time>.*)',
        '\$upstream_status': '(?P<upstream_status>.*)',
    })

    @staticmethod
    def dict_sub(text, d=LOG_PARAMS):
        """ Replace in 'text' non-overlapping occurences of REs whose patterns are keys
        in dictionary 'd' by corresponding values (which must be constant strings: may
        have named backreferences but not numeric ones). The keys must not contain
        anonymous matching-groups.
        Returns the new string.
        Thanks to Alex Martelli @
        http://stackoverflow.com/questions/937697/can-you-pass-a-dictionary-when-replacing-strings-in-python
        """
        if d != NginxParsing.LOG_SPECIAL_SYMBOLS:
            text = NginxParsing.dict_sub(text, NginxParsing.LOG_SPECIAL_SYMBOLS)

        # Create a regular expression  from the dictionary keys
        regex = re.compile("|".join("(%s)" % k for k in d))
        # Facilitate lookup from group number to value
        lookup = dict((i + 1, v) for i, v in enumerate(d.values()))
        # For each match, find which group matched and expand its value
        result = regex.sub(lambda mo: mo.expand(lookup[mo.lastindex]), text)

        return result

    @staticmethod
    def each_line_fun(compiled_regex1, line):

        line = line.strip()
        if line == "":
            return {}

        data = re.match(compiled_regex1, line)
        if not data:
            pass
            print('Parsing Error [{}]'.format(line))
        else:
            datadict = data.groupdict()
            if 'nginx_status' in datadict.get('request_request_uri', ""):
                return {}
            return datadict
        return {}

    @staticmethod
    def parse_log(line):
        log_format1 = """$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" 
        "$http_user_agent" "$http_x_forwarded_for" rt=$req_time ua="$upstream_addr" us="$upstream_status"
         ut="$upstream_response_time" ul="$upstream_response_length" cs=$upstream_cache_status"""
        # log_format2 = """$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent
        # "$http_referer" "$http_user_agent" """
        reg = NginxParsing.dict_sub(log_format1)
        compiled_regex1 = re.compile(reg, re.IGNORECASE)
        # compiled_regex2 = re.compile(NginxParsing.dict_sub(log_format2), re.IGNORECASE)
        parsed = NginxParsing.each_line_fun(compiled_regex1, line.strip())
        pparsed = lambda i: parsed.get(i, "")
        """"$remote_addr - $remote_user[$time_local] "$request" $status $body_bytes_sent
        "$http_referer" "$http_user_agent" "$http_x_forwarded_for"
        rt =$req_time
        ua = "$upstream_addr"
        us = "$upstream_status"
        ut = "$upstream_response_time"
        ul = "$upstream_response_length"
        cs =$upstream_cache_status
        """
        csv_res = {
            'time_local': datetime.strptime(pparsed('time_local'), '%d/%b/%Y:%H:%M:%S +%f') if pparsed(
                'time_local') != '' else datetime.now(),
            'status': int(pparsed('status')) if pparsed('status') != '' else 0,
            'request_request_uri': pparsed('request_request_uri'),
            'request_time': float(pparsed('request_time')) if pparsed('request_time') != '' else 0,
            'upstream_response_time': pparsed('upstream_response_time'),
            'remote_addr': pparsed('remote_addr'),
            'remote_user': pparsed('remote_user'),
            'referer': pparsed('http_referer'),
            'user_agent': pparsed('user_agent'),
        }
        # status = parsed.get('status', "")
        return csv_res


class NginxReporter:
    def __init__(self):
        pass

    @staticmethod
    def update_stats(line, stats):
        parsed_data = NginxParsing.parse_log(line)
        url = parsed_data['request_request_uri'].split('?')[0]
        stats['total_requests_count'].inc()
        stats['total_requests_count_by_service'].labels(service=url).inc()
        stats['requests_response_code_count'].labels(service=url, status=parsed_data['status']).inc()
        stats['total_request_by_user'].labels(user=parsed_data['remote_user']).inc()
        stats['total_processing_time'].inc(parsed_data['request_time'])
        stats['total_processing_time_by_url'].labels(service=url).inc(parsed_data['request_time'])
        if parsed_data['status'] not in [200, 204]:
            stats['failed_requests_count'].inc()
            stats['total_requests_failed_count_by_service'].labels(service=url).inc()
