import logging
import coloredlogs

from rpi_rf import RFDevice
"""
Yes, we need this. 

We need this because we need to keep track of the instances for different
RFDevice instances. Every Instance of an rfdevice represents a dedicated RF device,
but every plug can be attached to a different RF Device.
"""

class RFDeviceFactory(): 
    __instance = None

    @staticmethod
    def createRFDeviceFactory():
        if RFDeviceFactory.__instance is None:
            RFDeviceFactory()
        
        return RFDeviceFactory.__instance

    def __init__(self):
        if RFDeviceFactory.__instance is not None:
            raise Exception('The RFDevice Factory is a singleton. Use createRFDeviceFactory')

        self.__logger = logging.getLogger('RFDeviceFactory')
        coloredlogs.install(level='DEBUG', logger=self.__logger)

        self.__logger.debug('RFDeviceFactory singleton created')

        RFDeviceFactory.__instance = self
        self.__gpioDeviceMap = {}

    def createRFDevice(self, senderGpioPin, sendRepeat=10):
        if senderGpioPin in self.__gpioDeviceMap:
            return self.__gpioDeviceMap[senderGpioPin]

        else:
            newRFDevice = self.__initializeRfDevice(senderGpioPin, sendRepeat)
            self.__gpioDeviceMap[senderGpioPin] = newRFDevice
            return newRFDevice
    
    def __initializeRfDevice(self, senderGpioPin, sendRepeat):
        self.__logger.debug('Creating new RFDevice instance')
        self.__logger.debug('GPIO Pin: {}'.format(senderGpioPin))
        self.__logger.debug('Repeat count: {}'.format(sendRepeat))
        rfDevice = RFDevice(senderGpioPin)
        rfDevice.enable_tx()
        rfDevice.tx_repeat = sendRepeat
        return rfDevice
