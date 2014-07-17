# Module for blocking banned mime sites/hosts

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult


# API definitions starts here
class BannedSites:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned Sites"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedsitelist"
        self.host_list = loadFile(self.config_file)
        self.handler = "blockpage"
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
            req_host_parts = host.split('.')
            req_host_parts.reverse()
            for banned_host in self.host_list:
                banned_host_parts = banned_host.split('.')
                banned_host_parts.reverse()
                if len(banned_host_parts) > len(req_host_parts):
                    # req host is not a subdomain of banned host
                    continue
                matched = True
                for i in range(0, len(banned_host_parts)):
                    if banned_host_parts[i] != req_host_parts[i]:
                        # No match
                        matched = False
                if matched:
                    result.matched = True
                    result.category = self.category
                    result.criteria = host
                    return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return
