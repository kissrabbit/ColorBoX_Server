from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference,
)
import NetTime
from NetTime import ntplib
import Control
import gevent
from gevent import Greenlet
from gevent.event import Event
import serial
import DataBlocks
from DataBlocks import DataBlock

import logging
logger = logging.getLogger(name = None)

_ProcessResult = True


class SerialRx() :
    def __init__(self, type = '') :
        self.type = type

        self.isAvailable = True

        self._data = []
        self.block = DataBlock(type)

    def OpenSerial(self) :
        try :
            self._port = serial.Serial("/dev/ttyAMA0", baudrate = 115200, timeout = (Control.GetIntegration() + 3.0))
        except :
            self.isAvailable = False
            logger.error('Serial open error.')

    def Recive_Handle(self) :
        global _ProcessResult

        logger.info('Serial now working.')

        self._data = self._port.read(7388)

        if len(self._data) != 7388 :
            self._port.close()
            _ProcessResult = False

            logger.error('Serial recive not compile.')
            return
        else :
            self._port.close()
            logger.info('Recive Data Length: ' + str(len(self._data)))

            rawData = []
            result = 0
            for index in range(0, len(self._data), 2) :
                result = int(self._data[index + 1] << 8 | self._data[index])
                result = 3394 - result
                if result < 0 :
                    result = 0
                rawData.append(result)
           
            try :
                self.block.PutRaw(rawData)
                Save_NewRaw(rawData, self.type)
            except(ntplib.NTPException) :
                _ProcessResult = False
                logger.error('Time get error.')
                return
            except(FileNotFoundError) :
                _ProcessResult = False
                logger.error('File write error.')
                return

            _ProcessResult = True
    
    
def Save_NewRaw(value = [], type = '') :
    fileLocal = './Data/Raw/'
    
    realTime = NetTime.NetTime()
    realTime.UpdateTime()
    combine = realTime.Date + '\'\'' + realTime.Time

    fileName = type + '@' + \
                combine + \
                '.xlsx'

    logger.info('Saving Data...')

    workBook = Workbook()
    Sheet = workBook.active
    Sheet['A1'] = 'Voltage'

    for index in range(0, len(value)) :
        col = 'A' + str(index + 2)
        Sheet[col] = value[index]

    chart = LineChart()
    chart.title = 'Spectrum'
    chart.style = 2

    chart.y_axis.title = 'Voltage'
    chart.x_axis.title = 'cm-2'

    dataArea = Reference(Sheet, 
                         min_col = 1, max_col = 1, 
                         min_row = 1, max_row = len(value) + 1)

    chart.add_data(dataArea)
    Sheet.add_chart(chart, 'B2')

    workBook.save(filename = fileLocal + fileName)

    logger.info('Excel save at -> ' + fileLocal + fileName)


def CCD_GetRawData(type = '') :
    global _ProcessResult

    read = SerialRx(type)
    read.OpenSerial()

    if read.isAvailable is not False :
        if Control.StartConvert() is False :
            _ProcessResult = False
        else :
            pass
            job = gevent.spawn(read.Recive_Handle)
            job.join()
            DataBlocks.PickBlock(read.block)
    else :
        _ProcessResult = False

    return _ProcessResult

   