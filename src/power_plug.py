"""
Represents a PowerPlug with all the associated attributes.
"""

class PowerPlug():
    def __init__(self, codeOnOff, name='', pulselength=0, protocol=0):
        self.setOnOffCodes(codeOnOff)
        
        self.__name = name
        self.__pulselength = pulselength
        self.__protocol = protocol

    def setOnOffCodes(self, onOffCodes: tuple):
        if len(onOffCodes) != 2:
            raise AttributeError('Not all codes where given')
        self.__codeOn = onOffCodes[0]
        self.__codeOff = onOffCodes[1]

    def getOnOffCodes(self):
        return self.__codeOn, self.__codeOff

    def getName(self):
        return self.__name
    
    def setPulselength(self, newPulselength: int):
        self.__pulselength = newPulselength

    def getPulselength(self):
        return self.__pulselength

    def setProtocol(self, newProtocol: int):
        self.__protocol = newProtocol

    def getProtocol(self):
        return self.__protocol

    codes = property(getOnOffCodes, setOnOffCodes)
    name = property(getName)
    pulselength = property(getPulselength, setPulselength)
    protocol = property(getProtocol, setProtocol)
