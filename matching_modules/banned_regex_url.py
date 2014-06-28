# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

ROOT_PREFIX = "/home/justinschw/Documents/development/archangel/matching_modules"
config_file = ROOT_PREFIX + "/lists/bannedregexpurllist"
block_url = "http://127.0.0.1:8089/"
regex_list = loadFile(config_file)

# API definitions starts here

category = "Banned regex url"
handler = BlockPage(block_url)

# Scan algorithm
def scan(request):
    result = MatchResult()
    url = request.enc_req[1]
    for regex in regex_list:
        match = re.search(regex, url)
        if match != None:
            result.matched = True
            result.category = category
            result.criteria = regex
            return result
    # No match
    return result

# Stop as soon as a match is found
stop_after_match = True
