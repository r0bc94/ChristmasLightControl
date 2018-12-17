import logging
from rpi_rf import RFDevice

from .power_plug import PowerPlug

"""
This service handles the power plugs.
"""

class PowerPlugHandler():
    def __init__(self):
        self.__logger = logging.getLogger('Power Plug Service')
        self.__activatedPowerPlugs = []

    def turnOn(self, powerplug: PowerPlug):
        pass

    def __turnOn(self, powerplug: PowerPlug):
        self.__logger.info('Turning Plug {}'.format(powerplug.name))
        self.__logger.debug('Codes: {}'.format(powerplug.codes))
        