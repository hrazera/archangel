# Module for blocking banned mime types

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult


# API definitions starts here
class BannedMimeType:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'programroot')
        self.category = "Banned Mimetype"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedmimetypelist"
        self.mimetype_list = loadFile(self.config_file)
        self.handler = "blockpage"
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
