# Methods for blocking a page
import re

class ReplacePage:
    def handleRequest(self, req, data):
        req.set_icap_response(200)
        enc_req = req.enc_req[:]
        req.set_enc_request(' '.join(enc_req))
        for h in req.enc_req_headers:
            if h == 'content-length':
                # Set the content length after modification
                continue
            for v in req.enc_req_headers[h]:
                req.set_enc_header(h, v)
        # Copy the request body (in case of a POST for example)
        if not req.has_body:
            req.send_headers(False)
            return
        chunk_size = 0
        body = ''
        while True:
            chunk = req.read_chunk()
            chunk_size = max(chunk_size, len(chunk))
            body += chunk
            if chunk == '':
                break
        # Generate replaced body
        for rep in data:
            body = re.sub(rep.regex, rep.replace, body)
        req.set_enc_header('content-length', str(len(body)))
        req.send_headers(True)
        i = 0
        while i < len(body):
            req.write_chunk(body[i:i + chunk_size])
            i += chunk_size
        req.write_chunk('')

    def handleResponse(self, res, data):
        res.set_icap_response(200)
        res.set_enc_status(' '.join(res.enc_res_status))
        for h in res.enc_res_headers:
            if h == 'content-length':
                # Set the content length after modification
                continue
            for v in res.enc_res_headers[h]:
                res.set_enc_header(h, v)
        # Copy the request body (in case of a POST for example)
        if not res.has_body:
            res.send_headers(False)
            return
        chunk_size = 0
        body = ''
        while True:
            chunk = res.read_chunk()
            chunk_size = max(chunk_size, len(chunk))
            body += chunk
            if chunk == '':
                break
        # Generate replaced body
        for rep in data:
            body = re.sub(rep.regex, rep.replace, body)
        res.set_enc_header('content-length', str(len(body)))
        res.send_headers(True)
        i = 0
        while i < len(body):
            res.write_chunk(body[i:i + chunk_size])
            i += chunk_size
        res.write_chunk('')


