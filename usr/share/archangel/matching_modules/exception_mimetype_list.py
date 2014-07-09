# Module for allowing exception mime types

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult

# API definitions starts here
class ExceptionMimeType:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Exception Mimetype"
        self.config_file = self.ROOT_PREFIX + "/lists/exceptionmimetypelist"
        self.mimetype_list = loadFile(self.config_file)
        self.handler = "allowpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, response):
        result = MatchResult()
        if not 'content-type' in response.enc_res_headers:
            # No mimetype in response
            return result
        mime_types = response.enc_res_headers['content-type']
        for mime_type in mime_types:
            if mime_type.strip() in self.mimetype_list:
                result.matched = True
                result.category = self.category
                result.criteria = mime_type
                return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return
