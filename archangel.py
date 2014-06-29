#!/bin/env python

import random
import SocketServer

from pyicap import *
from ConfigParser import SafeConfigParser

# TODO: eventually have this set by the makefile
CONFIGFILE = '/home/justinschw/Documents/development/archangel/archangel.conf'
parser = SafeConfigParser()
parser.read(CONFIGFILE)

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
def load_http_scanner(scanner_name, handler_name):
    mod = __import__('matching_modules.' + scanner_name)
    prefix = 'mod.' + scanner_name
    initstr = prefix + '.init(parser, http_handlers["' + handler_name + '"])'
    eval(initstr)
    scan = eval(prefix + '.scan')
    stop_after_match = eval(prefix + '.stop_after_match')
    http_scanners[scanner_name] = (scan, stop_after_match)

for scanner_name, handler_name in parser.items('http_req_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, handler_name)
    http_req_scanners.append(scanner_name)

for scanner_name, handler_name in parser.items('http_res_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, handler_name)
    http_res_scanners.append(scanner_name)

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
        self.set_icap_response(200)

        print self.enc_req
        self.set_enc_request(' '.join(self.enc_req))
        for h in self.enc_req_headers:
            for v in self.enc_req_headers[h]:
                self.set_enc_header(h, v)

        # Copy the request body (in case of a POST for example)
        if not self.has_body:
            self.send_headers(False)
            return
        if self.preview:
            prevbuf = ''
            while True:
                chunk = self.read_chunk()
                if chunk == '':
                    break
                prevbuf += chunk
            if self.ieof:
                self.send_headers(True)
                if len(prevbuf) > 0:
                    self.write_chunk(prevbuf)
                self.write_chunk('')
                return
            self.cont()
            self.send_headers(True)
            if len(prevbuf) > 0:
                self.write_chunk(prevbuf)
            while True:
                chunk = self.read_chunk()
                self.write_chunk(chunk)
                if chunk == '':
                    break
        else:
            self.send_headers(True)
            while True:
                chunk = self.read_chunk()
                self.write_chunk(chunk)
                if chunk == '':
                    break

    def example_RESPMOD(self):
        self.set_icap_response(200)

        print self.enc_res_status
        self.set_enc_status(' '.join(self.enc_res_status))
        for h in self.enc_res_headers:
            for v in self.enc_res_headers[h]:
                self.set_enc_header(h, v)

        # The code below is only copying some data.
        # Very convoluted for such a simple task.
        # This thing needs a serious redesign.
        # Well, without preview, it'd be quite simple...
        if not self.has_body:
            self.send_headers(False)
            return
        if self.preview:
            prevbuf = ''
            while True:
                chunk = self.read_chunk()
                if chunk == '':
                    break
                prevbuf += chunk
            if self.ieof:
                self.send_headers(True)
                if len(prevbuf) > 0:
                    self.write_chunk(prevbuf)
                self.write_chunk('')
                return
            self.cont()
            self.send_headers(True)
            if len(prevbuf) > 0:
                self.write_chunk(prevbuf)
            while True:
                chunk = self.read_chunk()
                self.write_chunk(chunk)
                if chunk == '':
                    break
        else:
            self.send_headers(True)
            while True:
                chunk = self.read_chunk()
                self.write_chunk(chunk)
                if chunk == '':
                    break

port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
    while 1:
        server.handle_request()
except KeyboardInterrupt:
    print "Finished"
