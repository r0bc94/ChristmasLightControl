import yaml
import logging
import coloredlogs

from src.power_plug import PowerPlug
from src.gpio_device import GPIODevice

"""
This class represents the config parser, which reads the simple 
yaml file and converts the object into python objects.
"""
class ConfigParser():
    def __init__(self, configFilePath='./config.yaml'):
        self.__logger = logging.getLogger('ConfigParser')
        coloredlogs.install(level='DEBUG', logger=self.__logger)

        self.__filePath = configFilePath

    def parseConfigFile(self, args, configFilePath=''):
        """
        Parses the config file and returns a list of python objects.
        """
        self.__filePath = configFilePath if configFilePath else self.__filePath
        fileContent = ""
        try:
            with open(self.__filePath, 'r') as configFile:
                fileContent = configFile.read()
        except FileNotFoundError:
            self.__logger.error('No config file was found for: {}'.format(self.__filePath))
            raise
        except IOError as ioErr:
            self.__logger.exception('Error while trying to open the config file: {}'.format(ioErr))
            raise

        parsedConfiguration = None
        try:
            parsedConfiguration = yaml.load(fileContent)
            print(parsedConfiguration)
        except yaml.ScannerError as err:
            self.__logger.error('Failed to read the config file: {}'.format(err))
            raise
        return self.__parseTypes(parsedConfiguration, args)

    def __parseTypes(self, parsedConfigFile, args):
        """
        Iterates over all parsed keys and parses the devices.
        Returns a dict which associates every key with the parsed python object.
        """
        outDict = {}

        for curDevName, curDev in parsedConfigFile.items():
            try:
                devType = curDev['type']

                if devType == 'PowerPlug':
                    parsedPlug = self.__parsePowerPlug(curDev, curDevName, args)

                    if parsedPlug is not None:
                        outDict[curDevName] = parsedPlug
                
                elif devType == 'GPIODevice':
                    parsedGpioDev = self.__parseGpioDevice(curDev, curDevName)

                    if parsedGpioDev is not None:
                        outDict[curDevName] = parsedGpioDev
                
                else:
                    self.__logger.error('Unknown device type: {}, ignoring...'.format(curDevName))

            except KeyError:
                self.__logger.error('No Type for device {} given! Ignoring...'.format(curDevName))

        if len(outDict) == 0:
            self.__logger.warning('No devices where loaded! Please recheck your configuration.')

        return outDict

    def __parsePowerPlug(self, powerPlugRaw, devName, args):
        """
        Returns the PowerPlug object parsed from the passed object model.
        """
        outPlug = None
        try:
            codes = powerPlugRaw['codes']
            pulselength = powerPlugRaw['pulselength']
            protocol = powerPlugRaw['protocol']

            if args.enable_pin:
                outPlug = PowerPlug(codes,\
                    name=devName,\
                    pulselength=pulselength,\
                    protocol=protocol,\
                    setEnable=True,\
                    enablePin=args.enable_pin[0]
                )

            else:
                outPlug = PowerPlug(codes, name=devName, pulselength=pulselength, protocol=protocol)
        
        except KeyError as kerr:
            self.__logger.warning('Missing Property {}, skipping PowerPlug'.format(kerr))
    
        return outPlug

    def __parseGpioDevice(self, gpioDeviceRaw, devName):
        """
        Returns the GPIO object parsed from the passed object model.
        """
        outGpioDevice = None
        try:
            pin = gpioDeviceRaw['pin']

            outGpioDevice = GPIODevice(devName, pin)
        
        except KeyError as kerr:
            self.__logger.warning('Missing Property {}, skipping PowerPlug'.format(kerr))

        return outGpioDevice
