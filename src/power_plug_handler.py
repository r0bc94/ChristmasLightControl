import logging
import coloredlogs
import RPi.GPIO as GPIO
from rpi_rf import RFDevice
from time import sleep
from .rfdevice_factory import RFDeviceFactory

"""
This service handles the power plugs.
"""

class PowerPlugHandler():
    def __init__(self, senderGpioPin, sendRepeat=20, setEnablePin=False, enablePin=0):
        self.__logger = logging.getLogger().getChild('Power Plug Handler')

        self.__activatedPowerPlugs = []
        self.__needsEnablePin = setEnablePin
        self.__enablePin = enablePin
        self.__rfDevice = RFDeviceFactory.createRFDeviceFactory().createRFDevice(senderGpioPin, sendRepeat=sendRepeat)

    def turnOn(self, powerplug):
        codeOn = powerplug.codes[0]
        self.__sendDeviceCommand(codeOn, powerplug)

    def turnOff(self, powerplug):
        codeOff = powerplug.codes[1]
        self.__sendDeviceCommand(codeOff, powerplug)

    def __sendDeviceCommand(self, code, powerplug):
        pluselength = powerplug.pulselength
        protocol = powerplug.protocol

        self.__logger.info('Turning Plug {}'.format(powerplug.name))
        self.__logger.debug('Code: {}'.format(code))
        self.__logger.debug('Pulselenght: {}'.format(pluselength))
        self.__logger.debug('Protocol: {}'.format(protocol))
        
        # If the enable pin is set, pull it high before each transaction and
        # wait a bit
        if self.__needsEnablePin:
            self.__logger.debug(f'Setting ENABLED pin {self.__enablePin} to HIGH')
            GPIO.output(self.__enablePin, GPIO.HIGH)
            sleep(0.01)

        self.__rfDevice.tx_code(code, protocol, pluselength)

        if self.__needsEnablePin:
            self.__logger.debug(f'Setting ENABLED pin {self.__enablePin} to LOW')
            GPIO.output(self.__enablePin, GPIO.LOW)
