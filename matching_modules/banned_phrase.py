# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult
from utils.load_config_file import Phrase

# API definitions starts here
class BannedPhrase:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'programroot')
        self.category = "Banned phrase"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedphraselist"
        self.phrase_list = {}
        self.active_phrases = []
        strings = loadFile(self.config_file)
        for string in strings:
            phrase = Phrase()
            phrase.addPhrase(string)
            phrase_key = phrase.getKey()
            if not phrase_key in self.phrase_list.keys():
                self.phrase_list[phrase_key] = []
            self.phrase_list[phrase_key].append(phrase)
        self.handler = "blockpage"
        # Stop as soon as a match is found
        stop_after_match = True
    # Scan algorithm
    def scan(self, chunk):
        result = MatchResult()
        for char in chunk:
            # First advance activated phrases
            for phrase in self.active_phrases:
                if not phrase.advance(char):
                    if not phrase.active():
                        self.active_phrases.remove(phrase)
                if (phrase.matched()):
                    result.matched = True
                    result.category = self.category
                    phrase_string = ''
                    for word in phrase.words:
                        phrase_string += word[0] + ','
                    phrase_string = phrase_string[:-1]
                    result.criteria = phrase_string
                    # Reset active phrases before returning
                    for phrase in self.active_phrases:
                        phrase.reset()
                        self.active_phrases.remove(phrase)
                    return result
            # Now activate any inactive phrases that match this character
            for key in self.phrase_list.keys():
                if char in key:
                    for phrase in self.phrase_list[key]:
                        if not phrase in self.active_phrases and phrase.advance(char):
                            self.active_phrases.append(phrase)
        # No match
        for phrase in self.active_phrases:
            phrase.reset()
            self.active_phrases.remove(phrase)
        return result

