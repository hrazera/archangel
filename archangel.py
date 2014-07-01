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
def load_http_scanner(scanner_name, class_name):
    mod = __import__('matching_modules.' + scanner_name)
    mod_path = 'mod.' + scanner_name + '.' + class_name
    http_scanners[scanner_name] = eval(mod_path + '(parser)')

for scanner_name, class_name in parser.items('http_req_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, class_name)
    http_req_scanners.append(scanner_name)

for scanner_name, class_name in parser.items('http_res_scanners'):
    if not scanner_name in http_scanners.keys():
        load_http_scanner(scanner_name, class_name)
    http_res_scanners.append(scanner_name)

# TODO: load content scanners

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
        for scanner_name in http_req_scanners:
            scanner = http_scanners[scanner_name]
            result = scanner.scan(self)
            if result.matched:
                http_handlers[scanner.handler].handleRequest(self, result)
                if scanner.stop_after_scan:
                    return
        # TODO:
        # After this point, we will do content scanning
        # No match? allow page
        http_handlers['allowpage'].handleRequest(self, None)

    def example_RESPMOD(self):
        for scanner_name in http_res_scanners:
            scanner = http_scanners[scanner_name]
            result = scanner.scan(self)
            if result.matched:
                http_handlers[scanner.handler].handleResponse(self, result)
                if scanner.stop_after_scan:
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
