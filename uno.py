print('Application Initializing...')

from gevent import monkey
monkey.patch_all()
import gevent
import RawData
import ResultData
import SampleData
from XMLRPC import XMLRPCServer

from gevent.wsgi import WSGIServer
from flask import Flask
from flask import signals

import logging  
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

flaskCore = Flask(__name__)
flaskSignal = signals.Namespace()
xmlrpcServer = XMLRPCServer()

@flaskCore.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    logger.info('Application Start.')

    from subprocess import check_output, call
    try :
        out = check_output('lsof -i:80 -t', shell = True)
        pid = ''.join(list(filter(str.isdigit, str(out))))
        call('kill -9 ' + pid, shell = True)
        gevent.sleep(2)
        logger.info('Kill port.')
    except :
        pass

    #ipAddress = 'localhost'
    ipAddress = '192.168.222.112'

    xmlrpcServer.Initialize(ipAddress, 8080)
    xmlrpcServer.Rregister()
    xmlrpcServer.start()
    logger.info('XMLRPC server Start. ' + ipAddress + ':%d' %(8080))

    flaskCore.debug = True
    wsgiServer = WSGIServer((ipAddress, 80), flaskCore)
    logger.info('Flask server Start. ' + ipAddress + ':%d' %(80))
    wsgiServer.serve_forever()