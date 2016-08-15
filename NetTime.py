import gevent.timeout
import time
import ntplib

class NetTime :
    Date = ''
    Time = ''

    def __Get_RealTime(self) :
        with gevent.Timeout(10, False) as timeout:
            ntpClient = ntplib.NTPClient()
            response = ntpClient.request('202.108.6.95')

        localAreaTime = time.localtime(response.tx_time + 8 * 60 * 60)

        Date = '%u-%02u-%02u' %(localAreaTime.tm_year, localAreaTime.tm_mon, localAreaTime.tm_mday)
        Time = '%02u-%02u-%02u' %(localAreaTime.tm_hour, localAreaTime.tm_min, localAreaTime.tm_sec)

        return Date, Time

    def UpdateTime(self) :
        self.Date, self.Time = self.__Get_RealTime()

