from .device import Device
"""
A GPIO device is a simple device which can be turned on and off by 
setting a designated GPIO pin.
"""

class GPIODevice(Device):
    def __init__(self, name: str, pin: int):
        super().__init__(name)
        self.__pin = pin
    
    def getPin(self):
        return self.__pin
    
    def setPin(self, pin: int):
        self.__pin = pin

    pin = property(getPin, setPin)
