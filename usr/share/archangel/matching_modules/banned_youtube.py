# Module for blocking youtube videos based on a given criteria

import re
import urllib2

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

# API definitions starts here
class BannedYoutube:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned Youtube Video"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedyoutubelist"
        self.regex_list = loadFile(self.config_file)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
    # Scan algorithm
    def scan(self, request):
        result = MatchResult()
        url = request.enc_req[1]
        vid_id = ''
        m = re.search('youtube.com/watch?v=(.){11}', url) 
        if m != None:
            vid_id = url[m.start(0):m.end(0)][-11:]
        m = re.search('youtube.com/v/(.){11}', url)
        if m != None:
            vid_id = url[m.start(0):m.end(0)][-11:]
        if vid_id == '':
            # No youtube url present
            return result
        # Get info on youtube video
        data = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/'+vid_id+'?v=2&alt=json').read().lower()
        for regex in self.regex_list:
            match = re.search(regex, data)
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

