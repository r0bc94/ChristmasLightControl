import logging
from rpi_rf import RFDevice

from .power_plug import PowerPlug

"""
This service handles the power plugs.
"""

class PowerPlugHandler():
    def __init__(self, senderGpioPin, sendRepeat=10):
        self.__logger = logging.getLogger('Power Plug Service')
        self.__activatedPowerPlugs = []
        self.__rfDevice = self.__initializeRfDevice(senderGpioPin, sendRepeat)

    def turnOn(self, powerplug: PowerPlug):
        codeOn = powerplug.codes[0]
        self.__sendDeviceCommand(codeOn, powerplug)

    def turnOff(self, powerplug: PowerPlug):
        codeOff = powerplug.codes[1]
        self.__sendDeviceCommand(codeOff, powerplug)

    def __sendDeviceCommand(self, code, powerplug):
        pluselength = powerplug.pulselength
        protocol = powerplug.protocol

        self.__logger.info('Turning Plug {}'.format(powerplug.name))
        self.__logger.debug('Code: {}'.format(code))
        self.__logger.debug('Pulselenght: {}'.format(pluselength))
        self.__logger.debug('Protocol: {}'.format(protocol))
        
        self.__rfDevice.tx_code(code, protocol, pluselength)
