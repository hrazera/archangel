# Module for blocking banned URLs

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult

# API definitions starts here
class ExceptionUrl:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Exception URL"
        self.config_file = self.ROOT_PREFIX + "/lists/exceptionurllist"
        self.url_list = loadFile(self.config_file)
        self.handler = "allowpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, r):
        result = MatchResult()
        url = r.enc_req[1]
        for allowed_url in self.url_list:
            if allowed_url in url:
                result.matched = True
                result.category = self.category
                result.criteria = allowed_url
                return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return
