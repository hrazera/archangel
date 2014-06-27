# Module for blocking banned url regexes

from utils.load_config_file import loadfile
from utils.blockpage import BlockPage

config_file = "lists/bannedregexpurllist"

class banned_regex_url:
    def __init__(self):
        self.regex_list = loadFile(config_file);
