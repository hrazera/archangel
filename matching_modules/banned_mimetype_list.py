# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

ROOT_PREFIX = ''
config_file = ''
block_url = "http://127.0.0.1:8089/"
mimetype_list = None

# API definitions starts here

category = "Banned mime type"
handler = None

def init(parser, handler):
    ROOT_PREFIX = parser.get('app_config', 'programroot')
    config_file = ROOT_PREFIX + "/lists/bannedmimetypelist"
    mimetype_list = loadFile(config_file)
    handler = handler

# Scan algorithm
def scan(response):
    result = MatchResult()
    mime_type = response.enc_res_headers['content-type'].strip()
    if mime_type in mimetype_list:
        result.matched = True
        result.category = category
        result.criteria = mime_type
        return result
    # No match
    return result

# Stop as soon as a match is found
stop_after_match = True
