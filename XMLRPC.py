import gevent
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import threading
import socket
from socketserver import ThreadingMixIn

import RawData


class XMLRPCServer(threading.Thread):
    class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer) : pass 

    def Initialize(self, host, port) :
        self.server = self.ThreadingXMLRPCServer((host, port), allow_none = True)
    
    def Rregister(self) :
        self.server.register_function(RawData.CCD_GetRawData, 'GetRawData')

    def run(self):
        self.server.serve_forever()