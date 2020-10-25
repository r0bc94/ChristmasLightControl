import logging
import coloredlogs

import RPi.GPIO as GPIO

from .device import Device

"""
A GPIO device is a simple device which can be turned on and off by 
setting a designated GPIO pin.
"""

class GPIODevice(Device):
    def __init__(self, name: str, pin: int):
        super().__init__(name)
        self.__logger = logging.getLogger().getChild('GPIO Device')
        self.__pin = pin
        
        GPIO.setup(pin, GPIO.OUT)
    
    def getPin(self):
        return self.__pin
    
    def setPin(self, pin: int):
        self.__pin = pin

    def turnOn(self):
        self.__logger.info('Turning on GPIO Device {}'.format(self.name))
        self.__logger.debug('On Pin: {}'.format(self.__pin))
        GPIO.output(self.__pin, GPIO.HIGH)
    
    def turnOff(self):
        self.__logger.info('Turning off GPIO Device {}'.format(self.name))
        self.__logger.debug('On Pin: {}'.format(self.__pin))
        GPIO.output(self.__pin, GPIO.LOW)

    pin = property(getPin, setPin)
