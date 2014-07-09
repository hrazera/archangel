# Module for allowing exception HTTP header regexes

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult

# API definitions starts here
class ExceptionRegexUrl:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Exception Header Regex"
        self.config_file = self.ROOT_PREFIX + "/lists/exceptionregexpheaderlist"
        self.regex_list = loadFile(self.config_file)
        self.handler = "allowpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, request):
        result = MatchResult()
        url = request.enc_req[1]
        headers = None
        if len(request.enc_res_headers) > 0:
            # This is a respmod
            headers = request.enc_res_headers
        else:
            # This is a reqmod
            headers = request.enc_req_headers
        for regex in self.regex_list:
            for h in headers:
                for v in headers:
                    header_line = h + ': ' + v
                    match = re.search(regex, url)
                    if match != None:
                        result.matched = True
                        result.category = self.category
                        result.criteria = regex
                        return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return

