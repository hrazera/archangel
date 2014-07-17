1# Module for blocking youtube videos based on a given criteria

import re
import urllib2

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult

MAX_CACHE_SIZE = 2048

# API definitions starts here
class BannedYoutube:
    def __init__(self, parser):
        self.clean_cache = {}
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
        is_youtube=False
        if 'host' in request.enc_req_headers:
            for host in request.enc_req_headers['host']:
                if 'youtube' in host or 'ytimg' in host:
                    is_youtube=True
        if not is_youtube:
            return result
        m = re.search('watch\?v=(.){11}', url) 
        if m != None:
            vid_id = url[m.start(0):m.end(0)][-11:]
        m = re.search('v/(.){11}', url)
        if m != None:
            vid_id = url[m.start(0):m.end(0)][-11:]
        m = re.search('vi/(.){11}', url)
        if m != None:
            vid_id = url[m.start(0):m.end(0)][-11:]
        if vid_id == '':
            # No youtube url present
            return result
        # Check cache
        if vid_id in self.clean_cache:
            self.clean_cache[vid_id] += 1
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
        # Clean video; add to cache
        if len(self.clean_cache) == MAX_CACHE_SIZE:
            min_cache_key = min(self.clean_cache, key=self.clean_cache.get)
            del self.clean_cache[min_cache_key]
        if not vid_id in self.clean_cache:
            self.clean_cache[vid_id] = 1
        # No match
        return result
    # Dummy method
    def reset(self):
        return

