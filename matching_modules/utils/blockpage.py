# Methods for blocking a page
import urllib2

CHUNK_SIZE = 1024

class BlockPage:
    def __init__(self, blockUrl):
        self.blockUrl = blockUrl
    def handleRequest(self, req, data):
        req.set_icap_response(200)
        # get args for block page
        args = "blockpage.php?category="
        args += data.category
        args += "&criteria="
        args += data.criteria
        enc_req = req.enc_req[:]
        enc_req[1] = self.blockUrl + args
        req.set_enc_request(' '.join(enc_req))
        for h in req.enc_req_headers:
            for v in req.enc_req_headers[h]:
                req.set_enc_header(h, v)
        # Copy the request body (in case of a POST for example)
        if not req.has_body:
            req.send_headers(False)
            return
        while True:
            chunk = req.read_chunk()
            if chunk == '':
                break
    def handleResponse(self, res, data):
        res.set_icap_response(200)
        args = "blockpage.php?category="
        args += data.category
        args += "&criteria="
        args += data.criteria
        res.set_enc_status(' '.join(res.enc_res_status))
        bpContents = urllib2.urlopen(self.blockUrl + args).read()
        res.set_enc_header("content-length", str(len(bpContents)))
        res.set_enc_header("content-type", "text/html")
        i = 0
        res.send_headers(True)
        while True:
            x = res.read_chunk()
            if x == '':
                break
        while i < len(bpContents):
            res.write_chunk(bpContents[i:i+CHUNK_SIZE])
            i += CHUNK_SIZE
        res.write_chunk('')

