import logging
from time import sleep

import RPi.GPIO as GPIO
from rpi_rf import RFDevice

from .device import Device
from .rfdevice_factory import RFDeviceFactory

"""
Represents a PowerPlug with all the associated attributes.
"""

class PowerPlug(Device):
    def __init__(self, onCodes, offCodes, name='', pulselength=0, protocol=0, senderGpioPin=17, sendRepeat=20, setEnable=False, enablePin=0):
        super().__init__(name)
        
        self.__logger = logging.getLogger().getChild('Power Plug')

        self.__onCodes = onCodes
        self.__offCodes = offCodes
        self.__pulselength = pulselength
        self.__protocol = protocol
        self.__setEnablePin = setEnable
        self.__enablePin = enablePin

        self.__rfDevice = RFDeviceFactory.createRFDeviceFactory().createRFDevice(senderGpioPin, sendRepeat=sendRepeat)

    def getOnCodes(self):
        return self.__onCodes

    def getOffCodes(self):
        return self.__offCodes

    def setPulselength(self, newPulselength: int):
        self.__pulselength = newPulselength

    def getPulselength(self):
        return self.__pulselength

    def setProtocol(self, newProtocol: int):
        self.__protocol = newProtocol

    def getProtocol(self):
        return self.__protocol

    def turnOn(self):
        self.__logger.info('Turning ON plug {}'.format(self.name))
        for code in self.__onCodes:
            self.__sendDeviceCommand(code)

    def turnOff(self):
        self.__logger.info('Turning OFF plug {}'.format(self.name))
        for code in self.__offCodes:
            self.__sendDeviceCommand(code)

    def __sendDeviceCommand(self, code):
        self.__logger.debug('Code: {}'.format(code))
        self.__logger.debug('Pulselenght: {}'.format(self.__pulselength))
        self.__logger.debug('Protocol: {}'.format(self.__protocol))
        
        # If the enable pin is set, pull it high before each transaction and
        # wait a bit
        if self.__setEnablePin:
            self.__logger.debug(f'Setting ENABLED pin {self.__enablePin} to HIGH')
            GPIO.output(self.__enablePin, GPIO.HIGH)
            sleep(0.01)

        self.__rfDevice.tx_code(code, self.__protocol, self.__pulselength)

        if self.__setEnablePin:
            self.__logger.debug(f'Setting ENABLED pin {self.__enablePin} to LOW')
            GPIO.output(self.__enablePin, GPIO.LOW)

    onCodes = property(getOnCodes)
    offCodes = property(getOffCodes)
    pulselength = property(getPulselength, setPulselength)
    protocol = property(getProtocol, setProtocol)
    