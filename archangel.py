#!/bin/env python

import random
import re
import SocketServer

from pyicap import *
from ConfigParser import SafeConfigParser
from matching_modules.utils.load_config_file import loadFile
from matching_modules.utils.urlcache import UrlCache

# TODO: eventually have this set by the makefile
CONFIGFILE = '/home/justinschw/Documents/development/archangel/archangel.conf'
parser = SafeConfigParser()
parser.read(CONFIGFILE)

PROGRAM_ROOT = parser.get('app_config', 'programroot')
MAX_FILE_SCAN = parser.get('app_config', 'max_file_scan')
BLOCKHOST = parser.get('block_page_config', 'blockpageip') + ':' + \
            parser.get('block_page_config', 'blockpageport')
SND_CHUNK_SIZE = 8191
# Get list of scannable mime types
scannable_media = loadFile(PROGRAM_ROOT + '/lists/scannablemedia')

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
    content_res_scanners.append(scanner_name)

class ThreadingSimpleServer(SocketServer.ThreadingMixIn, ICAPServer):
    pass

def read_body(r):
    body = ''
    while True:
        chunk = r.read_chunk()
        if chunk == '':
            break
        body += chunk
    return body

def scan_http(r, scanner_list, request):
    # Returns (bool, bool) tuple indicating:
    # (stop_after_match, modified)
    modified = False
    for scanner_name in scanner_list:
        scanner = http_scanners[scanner_name]
        result = scanner.scan(r)
        scanner.reset()
        if result.matched:
            if request:
                http_handlers[scanner.handler].handleRequest(r, result)
            else:
                http_handlers[scanner.handler].handleResponse(r, result)
            if scanner.stop_after_match:
                return (True, False)
            else:
                modified = True
    return (False, modified)

def scan_content(r, body, scanner_list, request):
    # Returns (bool, bool) tuple indicating:
    # (stop_after_match, modified)
    modified = False
    for scanner_name in scanner_list:
        scanner = content_scanners[scanner_name]
        result = scanner.scan(body)
        scanner.reset()
        if result.matched:
            if request:
                http_handlers[scanner.handler].handleRequest(r, result)
            else:
                http_handlers[scanner.handler].handleResponse(r, result)
            if scanner.stop_after_match:
                return (True, False)
            else:
                modified = True
    return (False, modified)

def is_scannable(mime_type):
    for pattern in scannable_media:
        r = re.search(pattern, mime_type)
        if r != None:
            return True
    return False

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
        self.set_icap_response(200)

        self.set_enc_request(' '.join(self.enc_req))
        for h in self.enc_req_headers:
            for v in self.enc_req_headers[h]:
                self.set_enc_header(h, v)

        # HTTP Scanning
        result = scan_http(self, http_req_scanners, True)
        stop_after_match = result[0]
        modified = result[1]
        if stop_after_match:
            return

        # Don't scan content of unscannable media
        if 'content-type' in self.enc_req_headers:
            for mime_type in self.enc_req_headers['content-type']:
                if not is_scannable(mime_type):
                    print "ignoring"
                    http_handlers['allowpage'].handleRequest(self, None)
                    return

        # Don't scan content that is too long
        if 'content-length' in self.enc_req_headers:
            for length in self.enc_req_headers['content-length']:
                if length > MAX_FILE_SCAN:
                    http_handlers['allowpage'].handleRequest(self, None)
                    return

        # Content scanning
        body = ''
        if not self.has_body:
            self.send_headers(False)
            return
        if self.preview:
            preview = read_body(self)
            # Preliminary (preview) scan
            if len(body) > 0:
                result = scan_content(self, body, content_req_scanners, True)
                stop_after_match = result[0]
                modified = result[1]
                if stop_after_match:
                    return
            if self.ieof:
                body = preview
            else:
                if len(preview) > 0:
                    body += preview
                self.cont()
                body += read_body(self)
        else:
            body += read_body(self)
        # Full content scan
        if len(body) > 0:
            result = scan_content(self, body, content_req_scanners, True)
            stop_after_match = result[0]
            modified = result[1]
            if stop_after_match:
                return

        # Write body
        i = 0
        self.send_headers(True)
        if len(body) > 0:
            while i < len(body):
                self.write_chunk(body[i:i+SND_CHUNK_SIZE])
                i += SND_CHUNK_SIZE
        self.write_chunk('')

    def example_RESPMOD(self):
        self.set_icap_response(200)
        # If it's the block page, then allow
        if 'host' in self.enc_res_headers and \
           '127.0.0.1:8089' in self.enc_res_headers['host']:
            print "allowing block page"
            http_handlers['allowpage'].handleResponse(self, None)
            return

        self.set_enc_status(' '.join(self.enc_res_status))
        for h in self.enc_res_headers:
            for v in self.enc_res_headers[h]:
                self.set_enc_header(h, v)

        # HTTP Scanning
        result = scan_http(self, http_res_scanners, False)
        stop_after_match = result[0]
        modified = result[1]
        if stop_after_match:
            return

        # Don't scan content of unscannable media
        if 'content-type' in self.enc_res_headers:
            for mime_type in self.enc_res_headers['content-type']:
                if not is_scannable(mime_type):
                    print "ignoring"
                    http_handlers['allowpage'].handleResponse(self, None)
                    return

        # Don't scan content that is too big
        if 'content-length' in self.enc_res_headers:
            for length in self.enc_res_headers['content-length']:
                if length > MAX_FILE_SCAN:
                    http_handlers['allowpage'].handleResponse(self, None)
                    return

        # Content scanning
        body = ''
        if not self.has_body:
            self.send_headers(False)
            return
        if self.preview:
            preview = read_body(self)
            # Preliminary scan
            if len(body) > 0:
                result = scan_content(self, body, content_res_scanners, False)
                stop_after_match = result[0]
                modified = result[1]
                if stop_after_match:
                    return
            if self.ieof:
                body = preview
            else:
                if len(preview) > 0:
                    body += preview
                self.cont()
                body += read_body(self)
        else:
            body += read_body(self)
        # Full content scan
        if len(body) > 0:
            result = scan_content(self, body, content_res_scanners, False)
            stop_after_match = result[0]
            modified = result[1]
            if stop_after_match:
                return

        # Write body
        i = 0
        self.send_headers(True)
        if len(body) > 0:
            while i < len(body):
                self.write_chunk(body[i:i+SND_CHUNK_SIZE])
                i += SND_CHUNK_SIZE
        self.write_chunk('')


port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print "Finished"
