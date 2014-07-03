#!/bin/env python

import random
import SocketServer

from pyicap import *
from ConfigParser import SafeConfigParser

# TODO: eventually have this set by the makefile
CONFIGFILE = '/home/justinschw/Documents/development/archangel/archangel.conf'
parser = SafeConfigParser()
parser.read(CONFIGFILE)

MAX_FILE_SCAN = parser.get('app_config', 'max_file_scan')

http_handlers = {}
http_scanners = {}
content_scanners = {}
http_req_scanners = []
http_res_scanners = []
content_req_scanners = []
content_res_scanners = []

# Load handlers
for handler_name, class_name in parser.items('http_handlers'):
    mod = __import__('matching_modules.utils.' + handler_name)
    mod_path = 'mod.utils.' + handler_name + "." + class_name
    http_handlers[handler_name] = eval(mod_path + '(parser)')

# Load scanners
def load_http_scanner(scanner_name, class_name):
    mod = __import__('matching_modules.' + scanner_name)
    mod_path = 'mod.' + scanner_name + '.' + class_name
    http_scanners[scanner_name] = eval(mod_path + '(parser)')

def load_content_scanner(scanner_name, class_name):
    mod = __import__('matching_modules.' + scanner_name)
    mod_path = 'mod.' + scanner_name + '.' + class_name
    content_scanners[scanner_name] = eval(mod_path + '(parser)')

for scanner_name, class_name in parser.items('http_req_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, class_name)
    http_req_scanners.append(scanner_name)

for scanner_name, class_name in parser.items('http_res_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, class_name)
    http_res_scanners.append(scanner_name)

for scanner_name, class_name in parser.items('content_req_scanners'):
    if not scanner_name in content_scanners.keys():
        load_content_scanner(scanner_name, class_name)
    content_req_scanners.append(scanner_name)

for scanner_name, class_name in parser.items('content_res_scanners'):
    if not scanner_name in content_scanners.keys():
        load_content_scanner(scanner_name, class_name)
    content_req_scanners.append(scanner_name)

class ThreadingSimpleServer(SocketServer.ThreadingMixIn, ICAPServer):
    pass

class ICAPHandler(BaseICAPRequestHandler):

    def example_OPTIONS(self):
        self.set_icap_response(200)
        self.set_icap_header('Methods', 'RESPMOD,REQMOD')
        self.set_icap_header('Service', 'PyICAP Server 1.0')
        self.set_icap_header('Preview', '0')
        self.set_icap_header('Transfer-Preview', '*')
        self.set_icap_header('Transfer-Ignore', 'jpg,jpeg,gif,png,swf,flv')
        self.set_icap_header('Transfer-Complete', '')
        self.set_icap_header('Max-Connections', '100')
        self.set_icap_header('Options-TTL', '3600')
        self.send_headers(False)

    def example_REQMOD(self):
        modified = False
        # Need to copy request headers in case there is a modification
        for h in self.enc_req_headers:
            for v in self.enc_req_headers[h]:
                self.set_enc_header(h, v)
        # HTTP scanning
        for scanner_name in http_req_scanners:
            scanner = http_scanners[scanner_name]
            result = scanner.scan(self)
            if result.matched:
                http_handlers[scanner.handler].handleRequest(self, result)
                if scanner.stop_after_match:
                    return
                else:
                    modified = True
        # Content scanning
        chunks = []
        finished = False
        len_read = 0
        len_write = 0
        # TODO: change this so that we only scan the correct mime type
        if self.has_body:
            while True:
                chunk = self.read_chunk()
                len_read += len(chunk)
                if chunk == '':
                    finished = True
                    break
                for scanner_name in content_req_scanners:
                    scanner = content_scanners[scanner_name]
                    result = scanner.scan(chunk)
                    if result.matched:
                        http_handlers[scanner.handler].handleRequest(self, result)
                        if scanner.stop_after_match:
                            scanner.reset()
                            return
                        else:
                            modified = True
                            # chunk has been modified; get new size
                            len_write += len(chunk)
                chunks.append(chunk)
                if len_read >= MAX_FILE_SCAN:
                    break
            # Reset the scanners
            for scanner_name in content_req_scanners:
                content_scanners[scanner_name].reset()
        if modified:
            # Set new content length
            length = int(self.enc_req_headers['content-length'])
            length -= len_read
            length += len_write
            self.set_enc_header('content-length', str(length))
            # Send the modified request
            self.send_headers(True)
            for chunk in chunks:
                self.send_chunk(chunk)
            if finished:
                self.send_chunk('')
            else:
                while True:
                    chunk = self.read_chunk()
                    self.send_chunk(chunk)
                    if chunk == '':
                        break
        else:
            # No match? allow page
            self.send_headers(False)
            http_handlers['allowpage'].handleRequest(self, None)

    def example_RESPMOD(self):
        for scanner_name in http_res_scanners:
            scanner = http_scanners[scanner_name]
            result = scanner.scan(self)
            if result.matched:
                http_handlers[scanner.handler].handleResponse(self, result)
                if scanner.stop_after_match:
                    return
        # TODO:
        # After this point, we will do content scanning
        # No match? allow page
        http_handlers['allowpage'].handleResponse(self, None)


port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print "Finished"
