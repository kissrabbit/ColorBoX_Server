import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy

blockGroup = []

class DataBlock :
    def __init__(self, type = '') :
        self._rawData = []
        self._type = type
        self._result = 0.0

    def PutRaw(self, block = []) :
        self._rawData = block

    def GetRaw(self) :
        return self._rawData

    def GetRawLength(self) :
        return len(self._rawData)

    def DrawChart(self) :
        if self.GetLength() is not 0 :
            plt.plot(self._rawData)
            plt.ylabel('Voltage')
            plt.xlabel('Pixels')

    def GetType(self) :
        return self._type

    def SetResult(self, result = 0.0) :
        self._result = result

    def GetResult(self) :
        return self._result


def PickBlock(block) :
    new = copy.deepcopy(block)
    blockGroup.append(new)