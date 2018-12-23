import logging
import coloredlogs
from rpi_rf import RFDevice

from .rfdevice_factory import RFDeviceFactory

"""
This service handles the power plugs.
"""

class PowerPlugHandler():
    def __init__(self, senderGpioPin, sendRepeat=10):
        self.__logger = logging.getLogger('Power Plug Service')
        coloredlogs.install(level='DEBUG', logger=self.__logger)

        self.__activatedPowerPlugs = []
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
        
        self.__rfDevice.tx_code(code, protocol, pluselength)
