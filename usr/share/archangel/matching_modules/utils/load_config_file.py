# API for loading config files

class Phrase:
    def __init__(self):
        self.words = []
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
                    self.words.append(word)
                word = ''
            if x == '<':
                count += 1
    def getKey(self):
        key = ''
        for word in self.words:
            key += word[0]
        return key

def loadFile(filename):
    arr = []
    configFile = open(filename)
    for line in configFile:
        line = line.strip()
        begin_comment = line.find('#')
        if begin_comment >= 0:
            line = line[:begin_comment].strip()
        if line == '':
            continue
        elif line[0] == '#':
            continue
        elif line[0:9] == '.Include<':
            arr += loadFile(line[9:-1])
            continue
        arr.append(line)
    return arr


