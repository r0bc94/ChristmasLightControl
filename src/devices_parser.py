import yaml
import logging
import coloredlogs

from src.power_plug import PowerPlug
from src.gpio_device import GPIODevice
from src.ir_device import IRDevice

"""
This class represents the devices parser, which reads the simple 
yaml file and converts the object into python objects.
"""
class DevicesParser():
    def __init__(self, devicesFilePath='./devices.yaml'):
        self.__logger = logging.getLogger().getChild('Device Parser')
        self.__filePath = devicesFilePath

    def parseDevicesFile(self, args, devicesFilePath=''):
        """
        Parses the devices file and returns a list of python objects.
        """
        self.__filePath = devicesFilePath if devicesFilePath else self.__filePath
        fileContent = ""
        try:
            with open(self.__filePath, 'r') as devicesFile:
                fileContent = devicesFile.read()
        except FileNotFoundError:
            self.__logger.error('No devices file was found for: {}'.format(self.__filePath))
            raise
        except IOError as ioErr:
            self.__logger.exception('Error while trying to open the devices file: {}'.format(ioErr))
            raise

        parsedDevicesuration = None
        try:
            parsedDevicesuration = yaml.load(fileContent)
            print(parsedDevicesuration)
        except yaml.ScannerError as err:
            self.__logger.error('Failed to read the devices file: {}'.format(err))
            raise
        return self.__parseTypes(parsedDevicesuration, args)

    def __parseTypes(self, parsedDevicesFile, args):
        """
        Iterates over all parsed keys and parses the devices.
        Returns a dict which associates every key with the parsed python object.
        """
        outDict = {}

        for curDevName, curDev in parsedDevicesFile.items():
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

                elif devType == 'IRDevice':
                    parsedIrDev = self.__parseIrDevice(curDev, curDevName)

                    if parsedIrDev is not None:
                        outDict[curDevName] = parsedIrDev
                
                else:
                    self.__logger.error('Unknown device type: {}, ignoring...'.format(curDevName))

            except KeyError:
                self.__logger.error('No Type for device {} given! Ignoring...'.format(curDevName))

        if len(outDict) == 0:
            self.__logger.warning('No devices where loaded! Please recheck your devicesuration.')

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

            onCodes = []
            offCodes = []

            print(codes)

            if isinstance(codes, list):
                onCodes = [codes[0]]
                offCodes = [codes[1]]
            elif isinstance(codes, dict):
                # YAML actually interprets the strings 'ON' and 'OFF' as boolean values.
                onCodes = codes[True]
                offCodes = codes[False]
            else:
                raise AttributeError('The codes are provided in the wrong format.')

            if args.rf_enable_pin:
                outPlug = PowerPlug(onCodes, offCodes,\
                    name=devName,\
                    senderGpioPin=args.rf_gpio_pin,\
                    pulselength=pulselength,\
                    protocol=protocol,\
                    setEnable=True,\
                    enablePin=args.rf_enable_pin[0]
                )

            else:
                outPlug = PowerPlug(onCodes, offCodes, name=devName, senderGpioPin=args.rf_gpio_pin, pulselength=pulselength, protocol=protocol)
        
        except KeyError as kerr:
            self.__logger.warning('Missing Property {}, skipping PowerPlug'.format(kerr))
        
        except AttributeError as atrerr:
            self.__logger.warning('{}, skipping PowerPlug'.format(str(atrerr)))
    
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

    def __parseIrDevice(self, irDeviceRaw, devName):
        """
        Returns the parsed IR Device
        """
        options = dict(\
            powerKeyName = irDeviceRaw.get('powerkey_name'),\
            repeatCount = irDeviceRaw.get('repeat_count'),\
            timeout = irDeviceRaw.get('timeout')\
        )

        # Sanity check the provided arguments and build kwargs dict
        kwargs = {}
        for k, v in options.items():
            if v is None:
                continue

            if k == 'repeatCount' or k == 'timeout':
                if not isinstance(v, int):
                    self.__logger.warning(f'Argument {k} is set to a non integer value. Skipping IRDevice...')
                    return None

                kwargs[k] = int(v)

        return IRDevice(devName, **kwargs)
