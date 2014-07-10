# Module for allowing exception url regexes

import re

from utils.load_config_file import loadFile
from utils.matchresult import MatchResult
from utils.load_config_file import Phrase
from banned_phrase import ScanPhrase

# API definitions starts here
class ExceptionPhrase:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Exception Phrase"
        self.config_file = self.ROOT_PREFIX + "/lists/exceptionphraselist"
        self.phrase_list = {}
        strings = loadFile(self.config_file)
        for string in strings:
            phrase = Phrase()
            phrase.addPhrase(string)
            phrase_key = phrase.getKey()
            for char in phrase_key:
                if not char in self.phrase_list:
                    self.phrase_list[char] = []
                self.phrase_list[char].append(phrase)
        self.handler = "noop"
        # Stop as soon as a match is found
        self.stop_after_match = True
        # Scan each chunk individually
        self.scan_chunks = True
    # Scan algorithm
    def scan(self, chunk):
        body = chunk.lower()
        result = MatchResult()
        active_phrases = []
        for char in body:
            # First advance activated phrases
            for phrase in active_phrases:
                phrase.advance(char)
                if phrase.matched():
                    result.matched = True
                    result.category = self.category
                    phrase_string = ''
                    for word in phrase.phrase.words:
                        phrase_string += word + ", "
                    result.criteria = phrase_string[:-2]
                    return result
                elif not phrase.active():
                    # Remove from active list
                    active_phrases.remove(phrase)
            # Now activate any inactive phrases that match this character
            if char in self.phrase_list:
                for phrase in self.phrase_list[char]:
                    is_active = False
                    for scan_phrase in active_phrases:
                        if scan_phrase.phrase == phrase:
                            is_active = True
                    if not is_active:
                        # Add to active phrases
                        scan_phrase = ScanPhrase(phrase)
                        scan_phrase.advance(char)
                        active_phrases.append(scan_phrase)
        # No match
        return result
    # Dummy method
    def reset(self):
        return
