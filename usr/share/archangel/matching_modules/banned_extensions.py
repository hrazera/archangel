# Module for blocking banned extensions

import re
import urlparse, os

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
        path = urlparse.urlparse(url).path
        parts = os.path.splitext(path)
        ext = parts[len(parts)-1]
        if ext in self.extension_list:
            result.matched = True
            result.category = self.category
            result.criteria = ext
            return result
        # No match
        return result
    # Dummy method
    def reset(self):
        return

