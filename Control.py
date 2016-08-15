import smbus
from subprocess import call

import logging
logger = logging.getLogger(name = None)

_bus = smbus.SMBus(1)
_DeviceAddress = 0x20
_ControlRegister = 0x02
_IntegrationRegister = 0x01

_IntegrationTime = 50

def SetIntegration(val = 10) :
    global _IntegrationTime
    _IntegrationTime = val

    returnCode = call('i2cset -y 1 0x20 0x01 ' + str(val) + ' w', shell = True)
    if returnCode is 0 :
        logger.info('Set Integration done.')
    else :
        logger.error('Set Integration error.')
        return False
    return True


def StartConvert() :
    try :
        _bus.write_byte_data(_DeviceAddress, _ControlRegister, 0x01)
        logger.info('Convert Start done.')
    except :
        logger.error('Convert Start error.')
        return False
    return True


def GetIntegration() :
    return float(_IntegrationTime / 1000)