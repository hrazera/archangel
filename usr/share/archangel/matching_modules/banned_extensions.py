# Module for blocking banned extensions

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

# API definitions starts here
class BannedExtensions:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned Extension"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedextensionlist"
        self.extension_list = loadFile(self.config_file)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, request):
        result = MatchResult()
        url = request.enc_req[1].lower()
        for banned_extension in self.extension_list:
            if banned_extension in url:
                result.matched = True
                result.category = self.category
                result.criteria = banned_extension
                return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return

