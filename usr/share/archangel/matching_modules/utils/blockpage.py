# Methods for blocking a page
import urllib2
import urllib
import logging
from logging import handlers

CHUNK_SIZE = 1024

class BlockPage:
    def __init__(self, parser):
        ip = parser.get('block_page_config', 'blockpageip')
        port = parser.get('block_page_config', 'blockpageport')
        self.blockUrl = 'http://' + ip + ':' + port + '/'
        self.logFileName = parser.get('app_config', 'logfile')
        self.log = logging.getLogger('blockpage')
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
        handler_stream = logging.StreamHandler()
        handler_stream.setLevel(logging.INFO)
        self.log.addHandler(handler_stream)
        handler_file = \
            logging.handlers.RotatingFileHandler( \
                self.logFileName, 'a', \
                parser.get('app_config', 'logfile_max_size'), \
                parser.get('app_config', 'logfile_backup_count'))
        #handler_file = logging.FileHandler(self.logFileName)
        handler_file.setFormatter(formatter)
        self.log.addHandler(handler_file)
    def handleRequest(self, req, data):
        # log block page
        req_url = req.enc_req[1]
        if not req.enc_headers['host'][0] in req_url:
            req_url = req.enc_headers['host'][0] + '/' + req_url
        self.log.info('Blocked url: ' + req_url + ' category: "' \
                 + data.category + '" criteria: ' + data.criteria)
        # get args for block page
        args = {}
        args['category'] = data.category
        args['criteria'] = data.criteria
        enc_req = req.enc_req[:]
        enc_req[0] = 'GET'
        enc_req[1] = self.blockUrl + 'blockpage.php?' + urllib.urlencode(args)
        req.set_enc_request(' '.join(enc_req))
        #if 'content-type' in req.enc_headers:
        #    del req.enc_headers['content-type']
        #if 'content-length' in req.enc_headers:
        #    del req.enc_headers['content-length']
        req.send_headers(False)
    def handleResponse(self, res, data):
        # log block page
        res_url = res.enc_headers['host'][0]
        self.log.info('Blocked content: ' + res_url + ' category: "' \
                 + data.category + '" criteria: ' + data.criteria)
        # get args for block page
        args = {}
        args['category'] = data.category
        args['criteria'] = data.criteria
        argstring = 'blockpage.php?' + urllib.urlencode(args)
        res.set_enc_status(' '.join(res.enc_res_status))
        bpContents = urllib2.urlopen(self.blockUrl + argstring).read()
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

