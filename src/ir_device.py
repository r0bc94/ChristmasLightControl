import logging
import coloredlogs

from .device import Device
from .lirc_service import runLircCommand


class IRDevice(Device):
    def __init__(self, name: str, powerKeyName='KEY_POWER', repeatCount=1, timeout=2):
        self.__logger = logging.getLogger().getChild('IR_Device')
        coloredlogs.install(level='DEBUG', logger=self.__logger)

        self.__logger.debug(f'Creating new IRDevice')
        self.__logger.debug(f'Name: {name}')
        self.__logger.debug(f'repeatCount: {repeatCount}')
        self.__logger.debug(f'timeout: {timeout}')

        self.__name = name
        self.__repeatCount = repeatCount
        self.__timeout = timeout

    def turnOn(self):
        self.__toggleDevice()

    def turnOff(self):
        self.__toggleDevice()

    def sendKey(self, key: str):
        """
        Sends the given key to the ir device.
        """
        self.__logger.info(f'Sending Key {key} to IR device: {self.__name}')
        self.__logger.debug(f'repeatCount: {self.__repeatCount}')
        self.__logger.debug(f'timeout: {self.__timeout}')
        runLircCommand(self.__name, key, repeatCount=self.__repeatCount, timeout=self.__timeout)

    def __toggleDevice(self):
        """
        Toggles the device on and off by just sending the code
        which is defined for the KEY_POWER in the lirc config.
        """
        self.__logger.info(f"Toggling IR Device: {self.__name}")
        runLircCommand(self.__name, 'KEY_POWER', repeatCount=self.__repeatCount, timeout=self.__timeout)
