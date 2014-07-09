# Module for blocking banned URLs

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult

# API definitions starts here
class BannedUrl:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned URL"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedurllist"
        self.url_list = loadFile(self.config_file)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, r):
        result = MatchResult()
        url = r.enc_req[1]
        for banned_url in self.url_list:
            if banned_url in url:
                result.matched = True
                result.category = self.category
                result.criteria = banned_url
                return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return
