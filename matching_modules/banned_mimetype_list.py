# Module for blocking banned mime types

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult


# API definitions starts here
class BannedMimeType:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'programroot')
        self.category = "Banned mime type"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedmimetypelist"
        self.mimetype_list = loadFile(self.config_file)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        stop_after_match = True
    # Scan algorithm
    def scan(self, request):
        result = MatchResult()
        mime_type = response.enc_res_headers['content-type'].strip()
        if mime_type in mimetype_list:
            result.matched = True
            result.category = self.category
            result.criteria = mime_type
            return result
        # No match
        return result

