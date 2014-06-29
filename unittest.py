# Test the banned regex url module

class TestReq:
    def __init__(self):
        self.enc_req = []

class TestRes:
    def __init__(self):
        self.enc_res_headers = {}

matchmod = __import__('matching_modules.banned_regex_url')
req = TestReq()
req.enc_req = ["GET", "mypage.php?anonymizer=true", "HTTP/1.1"]
result = matchmod.banned_regex_url.scan(req)
if result.matched == True and result.category == 'Banned regex url':
    print "Test Passed"
else:
    print "Test Failed"

res = TestRes()
mimematcher = __import__('matching_modules.banned_mimetype_list')
res.enc_res_headers['content-type'] = 'audio/mpeg'
result = matchmod.banned_mimetype_list.scan(res)
print result
print result.matched
print result.category
if result.matched == True and result.category == 'Banned mime type':
    print "Test Passed"
else:
    print "Test Failed"


