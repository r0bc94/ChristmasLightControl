from .device import Device
from .power_plug_handler import PowerPlugHandler
"""
Represents a PowerPlug with all the associated attributes.
"""

class PowerPlug(Device):
    def __init__(self, codeOnOff, name='', pulselength=0, protocol=0, senderGpioPin=17, sendRepeat=10, setEnable=False, enablePin=0):
        super().__init__(name)
        self.setOnOffCodes(codeOnOff)
        
        self.__pulselength = pulselength
        self.__protocol = protocol

        self.__handler = PowerPlugHandler(senderGpioPin, sendRepeat=sendRepeat, setEnablePin=setEnable, enablePin=enablePin)

    def setOnOffCodes(self, onOffCodes: tuple):
        if len(onOffCodes) != 2:
            raise AttributeError('Not all codes where given')
        self.__codeOn = onOffCodes[0]
        self.__codeOff = onOffCodes[1]

    def getOnOffCodes(self):
        return self.__codeOn, self.__codeOff

    def setPulselength(self, newPulselength: int):
        self.__pulselength = newPulselength

    def getPulselength(self):
        return self.__pulselength

    def setProtocol(self, newProtocol: int):
        self.__protocol = newProtocol

    def getProtocol(self):
        return self.__protocol

    def turnOn(self):
        self.__handler.turnOn(self)

    def turnOff(self):
        self.__handler.turnOff(self)

    codes = property(getOnOffCodes, setOnOffCodes)
    pulselength = property(getPulselength, setPulselength)
    protocol = property(getProtocol, setProtocol)
    