# Module for blocking banned url regexes

import re

from utils.load_config_file import loadFile
from utils.blockpage import BlockPage
from utils.matchresult import MatchResult
from utils.load_config_file import Phrase

class WordMap:
    def __init__(self):
        self.words = {}
        self.sorted = []
    def add(self, phrase):
        for word in phrase.words:
            if not word in self.words:
                self.words[word] = [phrase]
            else:
                self.words[word].append(phrase)
            i = 0
    def sort(self):
        del self.sorted[:]
        for word in self.words:
            i = 0
            for word2 in self.sorted:
                if len(self.words[word2]) <= len(self.words[word]):
                    break
                i += 1
            self.sorted.insert(i, word)

# API definitions starts here
class BannedPhrase:
    def __init__(self, parser):
        self.ROOT_PREFIX = parser.get('app_config', 'confdir')
        self.category = "Banned Phrase"
        self.config_file = self.ROOT_PREFIX + "/lists/bannedphraselist"
        self.wordMap = WordMap()
        strings = loadFile(self.config_file)
        for string in strings:
            phrase = Phrase()
            phrase.addPhrase(string)
            self.wordMap.add(phrase)
        self.wordMap.sort()
        self.handler = "blockpage"
        # Stop as soon as a match is found
        self.stop_after_match = True
        # Scan each chunk individually
        self.scan_chunks = True
        
    # Scan algorithm
    def scan(self, chunk):
        body = chunk.lower()
        result = MatchResult()
        phraseCounts = {}
        for word in self.wordMap.sorted:
            if re.search(word, body):
                for phrase in self.wordMap.words[word]:
                    if not phrase in phraseCounts:
                        phraseCounts[phrase] = 1
                    else:
                        phraseCounts[phrase] += 1
                    if phraseCounts[phrase] == len(phrase.words):
                        result.matched = True
                        result.category = self.category
                        phrase_string = ''
                        for word in phrase.words:
                            phrase_string += word + ', '
                        result.criteria = phrase_string[:-2]
        # No match
        return result
    # Dummy method
    def reset(self):
        return
