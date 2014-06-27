class Req:
    def __init__(self):
        self.enc_req = ['GET', '/', 'HTTP/1.1']
        self.icap_res = 0
        self.enc_req_headers = {"Content-Length":"187"}
        self.snd_h = False
        self.has_body = False
    def set_enc_request(self, x):
        self.enc_req = x
    def set_enc_header(self, h, v):
        self.enc_req_headers[h] = v
    def set_icap_response(self, x):
        self.icap_res = x
    def send_headers(self, x):
        self.snd_h = x

class Res:
    def __init__(self):
        self.enc_res = ['HTTP/1.1', '200', 'OK']
        self.icap_res = 0
        self.enc_res_headers = {"Content-Length":"187"}
        self.snd_h = False
        self.has_body = False
    def set_enc_status(self, x):
        self.enc_res = x
    def set_enc_header(self, h, v):
        self.enc_res_headers[h] = v
    def set_icap_response(self, x):
        self.icap_res = x
    def send_headers(self, x):
        self.snd_h = x
