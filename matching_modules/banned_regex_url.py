# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

# API definitions starts here
class BannedRegexUrl:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'programroot')
        self.category = "Banned regex url"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedregexpurllist"
        self.regex_list = loadFile(self.config_file)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        stop_after_match = True
    # Scan algorithm
    def scan(self, request):
        result = MatchResult()
        host = request.enc_req_headers['host'].strip()
        url = request.enc_req[1]
        for regex in self.regex_list:
            match = re.search(regex, host + '/' + url)
            if match != None:
                result.matched = True
                result.category = self.category
                result.criteria = regex
                return result
        # No match
        return result

