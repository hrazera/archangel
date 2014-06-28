# Test the banned regex url module

class TestReq:
    def __init__(self):
        self.enc_req = []

matchmod = __import__('matching_modules.banned_regex_url')
req = TestReq()
req.enc_req = ["GET", "mypage.php?anonymizer=true", "HTTP/1.1"]
result = matchmod.banned_regex_url.scan(req)
if result.matched == True and result.category == 'Banned regex url':
    print "Test Passed"
else:
    print "Test Failed"
