# Module for allowing exception mime sites/hosts

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult


# API definitions starts here
class ExceptionSites:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Exception Sites"
        self.config_file = self.ROOT_PREFIX + "/lists/exceptionsitelist"
        self.host_list = loadFile(self.config_file)
        self.handler = "allowpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, r):
        result = MatchResult()
        hosts = None
        if 'host' in r.enc_req_headers:
            hosts = r.enc_req_headers['host']
        elif 'host' in r.enc_res_headers:
            hosts = r.enc_res_headers['host']
        if hosts == None:
            # No host in headers
            return result
        for host in hosts:
            for allowed_host in self.host_list:
                if allowed_host.strip() in host.strip():
                    result.matched = True
                    result.category = self.category
                    result.criteria = host
                    return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return
