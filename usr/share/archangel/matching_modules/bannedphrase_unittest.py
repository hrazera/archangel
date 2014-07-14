from ConfigParser import SafeConfigParser
from banned_phrase import BannedPhrase

parser = SafeConfigParser()
parser.read('/etc/archangel/archangel.conf')

bp = BannedPhrase(parser)
chunk = "The quick brown fox jumped over the lazy dog"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "The quick brown fox jumped over the lazy puppies"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "The quick brown fox loved to jump over the lazy dog"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "I love my puppy"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "I love my puppy"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "The quick brown fox jumped over the lazy dog"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk

chunk = "The puppy loves to jump over lazy foxes"
m = bp.scan(chunk)
print "matched: " + str(m.matched)
bp.reset()
print chunk
