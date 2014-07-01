# API for loading config files

class Phrase:
    def __init__(self):
        self.words = []
        self.active_word = 0
        self.active_position = 0
    def addPhrase(self, line):
        isWord = False
        count = 0
        word = ''
        for x in line:
            if x == '>':
                count -= 1
            if count > 0:
                word += x
            else:
                if word != '':
                    self.words.append((word,0))
                word = ''
            if x == '<':
                count += 1
    def advance(self, char):
        activated = False
        for i in range(0, len(self.words)):
            item = self.words[i]
            word = item[0]
            pos = item[1]
            if pos >= len(word):
                continue
            if word[pos] == char:
                self.words[i] = (word, pos + 1)
                activated = True
            else:
                # No match; reset this word
                self.words[i] = (word, 0)
        return activated
    def matched(self):
        match = True
        for item in self.words:
            word = item[0]
            pos = item[1]
            if pos < len(word):
                match = False
        return match
    def reset(self):
        for i in range(0, len(self.words)):
            item = self.words[i]
            word = item[0]
            self.words[i] = (word, 0)
    def getKey(self):
        first_letters = []
        for item in self.words:
            first_letters.append(item[0][0])
        first_letters.sort()
        key = ''
        for letter in first_letters:
            key += letter
        return key

def loadFile(filename):
    arr = []
    configFile = open(filename)
    for line in configFile:
        line = line.strip()
        if line == '':
            continue
        elif line[0] == '#':
            continue
        elif line[0:9] == '.Include<':
            arr += loadFile(line[9:-1])
        arr.append(line)
    return arr


