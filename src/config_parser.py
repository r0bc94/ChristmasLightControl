import yaml
import logging

from src.power_plug import PowerPlug
from src.gpio_device import GPIODevice

"""
This class represents the config parser, which reads the simple 
yaml file and converts the object into python objects.
"""
class ConfigParser():
    def __init__(self, configFilePath='./config.yaml'):
        self.__logger = logging.getLogger('ConfigParser')
        self.__filePath = configFilePath

    def parseConfigFile(self, configFilePath=''):
        """
        Parses the config file and returns a list of python objects.
        """
        self.__filePath = configFilePath if configFilePath else self.__filePath
        fileContent = ""
        try:
            with open(self.__filePath, 'r') as configFile:
                fileContent = configFile.read()
        except FileNotFoundError:
            self.__logger.error('No config file was found in {}'.format(self.__filePath))
            raise
        except IOError as ioErr:
            self.__logger.exception('Error while trying to open the config file: {}'.format(ioErr))
            raise

        parsedConfiguration = None
        try:
            parsedConfiguration = yaml.load(fileContent)
        except yaml.ScannerError as err:
            self.__logger.error('Failed to read the config file: {}'.format(err))
            raise
        return self.__parseTypes(parsedConfiguration)

    def __parseTypes(self, parsedConfigFile):
        """
        Looks up all specified device types in the parsed config file and calls the
        correct parsing method
        """
        outDict = {}
        if 'PowerPlugs' in parsedConfigFile:
            powerPlugsRaw = parsedConfigFile['PowerPlugs']
            parsedPowerPlugs = self.__parsePowerPlugs(powerPlugsRaw)

            if len(parsedPowerPlugs) == 0:
                self.__logger.warning('Power Plugs where defined but none where loaded. Please recheck your configuration!')

            outDict['PowerPlugs'] = parsedPowerPlugs
            

        if 'GPIODevices' in parsedConfigFile:
            gpioDevicesRaw = parsedConfigFile['GPIODevices']
            parsedGpioDevices = self.__parseGpioDevices(gpioDevicesRaw)

            if len(parsedGpioDevices) == 0:
                self.__logger.warning('GPIO Devices where defined but none where loaded. Please recheck your configuration!')

            outDict['GPIODevices'] = parsedGpioDevices
        
        return outDict

    def __parsePowerPlugs(self, powerPlugList):
        """
        Creates a list of gpio device python objects from the passed raw object model.
        """
        outPlugs = []
        for currentPlug in powerPlugList:
            try:
                name = currentPlug['name']
                codes = currentPlug['codes']
                pulselength = currentPlug['pulselength']
                protocol = currentPlug['protocol']

                outPlug = PowerPlug(codes, name=name, pulselength=pulselength, protocol=protocol)
                outPlugs.append(outPlug)
            
            except KeyError as kerr:
                self.__logger.warning('Missing Property {}, skipping PowerPlug'.format(kerr))
                continue
        
        return outPlugs

    def __parseGpioDevices(self, gpioDevicesList):
        """
        Creates a list of gpio device python objects from the passed raw object model.
        """
        outGpioDevices = []
        for currentDevice in gpioDevicesList:
            try:
                name = currentDevice['name']
                pin = currentDevice['pin']

                outGpioDevice = GPIODevice(name, pin)
                outGpioDevices.append(outGpioDevice)
            
            except KeyError as kerr:
                self.__logger.warning('Missing Property {}, skipping PowerPlug'.format(kerr))
                continue

        return outGpioDevices
