# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult
from utils.load_config_file import Phrase

class ScanPhrase:
    def __init__(self, phrase):
        self.words = []
        for word in phrase.words:
            self.words.append((word, 0))
        self.phrase = phrase
    def advance(self, char):
        result = False
        for i in range(0, len(self.words)):
            word = self.words[i][0]
            pos = self.words[i][1]
            if pos >= len(word):
                result = True
                continue
            if word[pos] == char:
                self.words[i] = (word, pos + 1)
                result = True
            else:
                self.words[i] = (word, 0)
        return result
    def matched(self):
        result = True
        for item in self.words:
            word = item[0]
            pos = item[1]
            if pos < len(word):
                result = False
        return result
    def active(self):
        for word in self.words:
            if word[1] > 0:
                return True
        return False

# API definitions starts here
class BannedPhrase:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned Phrase"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedphraselist"
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
        self.handler = "blockpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
        # Scan each chunk individually
        self.scan_chunks = True
    # Scan algorithm
    def scan(self, chunk):
        result = MatchResult()
        active_phrases = []
        for char in chunk:
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
