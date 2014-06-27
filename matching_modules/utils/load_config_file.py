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

def loadFile(filename):
    arr = []
    configFile = open(filename)
    for line in configFile:
        if line[0] == '#':
            continue
        elif line[0:9] == '.Include<':
            arr += loadFile(line[9:-1])
        arr.append(line)
    return arr


