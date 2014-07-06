# Methods for blocking a page
import urllib2

CHUNK_SIZE = 1024

class BlockPage:
    def __init__(self, parser):
        ip = parser.get("block_page_config", "blockpageip")
        port = parser.get("block_page_config", "blockpageport")
        self.blockUrl = "http://" + ip + ":" + port + "/"
    def handleRequest(self, req, data):
        # get args for block page
        args = "blockpage.php?category="
        args += data.category
        args += "&criteria="
        args += data.criteria
        enc_req = req.enc_req[:]
        enc_req[0] = 'GET'
        enc_req[1] = self.blockUrl + args
        req.set_enc_request(' '.join(enc_req))
        #if 'content-type' in req.enc_headers:
        #    del req.enc_headers['content-type']
        #if 'content-length' in req.enc_headers:
        #    del req.enc_headers['content-length']
        req.send_headers(False)
    def handleResponse(self, res, data):
        # get args for block page
        args = 'blockpage.php?category='
        args += data.category
        args += '&criteria='
        args += data.criteria
        res.set_enc_status(' '.join(res.enc_res_status))
        bpContents = urllib2.urlopen(self.blockUrl + args).read()
        res.enc_headers.clear()
        res.set_enc_header('content-length', str(len(bpContents)))
        res.set_enc_header('content-type', 'text/html')
        res.set_enc_header('connection', 'close')
        i = 0
        res.send_headers(True)
        while i < len(bpContents):
            res.write_chunk(bpContents[i:i+CHUNK_SIZE])
            i += CHUNK_SIZE
        res.write_chunk('')

