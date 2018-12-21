import pytest
import logging
from collections import OrderedDict

from src.config_parser import ConfigParser

from src.power_plug import PowerPlug
from src.gpio_device import GPIODevice

class TestConfigParser():
    
    @pytest.fixture(scope = 'session')
    def configParser(self):
        return ConfigParser()

    def testParseEverything(self, configParser):
        print('It should read a good config file, which contains one PowerPlug and one GPIO Device.')

        expectedResult = {
            'PowerPlug1': PowerPlug(
                [123, 456],
                name='PowerPlug1',
                protocol=1,
                pulselength=234),
            'GPIODevice1': GPIODevice('GPIODevice1', 2)
        }

        parsedConfig = configParser.parseConfigFile(configFilePath='test/config_parser_tests/fixtures/everything.yaml')
        
        assert isinstance(parsedConfig, dict)
        assert len(parsedConfig) == 2

        self.__checkResultsNew(parsedConfig, expectedResult)

    def testParseFaultyPPs(self, configParser):
        print('It should at least parse all GPIODevices, even if the PowerPlugs format is wrong')

        expectedResult = {
            'GPIODevice1': GPIODevice('GPIODevice1', 2)
        }

        parsedConfig = configParser.parseConfigFile(configFilePath='test/config_parser_tests/fixtures/faulty_powerplugs.yaml')

        assert isinstance(parsedConfig, dict)
        assert len(parsedConfig) == 1

        self.__checkResults(parsedConfig, expectedResult)

    def testParseFaultyGPIODevs(self, configParser):
        print('It should at least parse all PowerPlugs, even if the GPIODevice format is wrong')

        expectedResult = {
            'PowerPlug1': PowerPlug(
                            [123, 567],
                            name='PowerPlug1',
                            protocol=0,
                            pulselength=567)
        }

        parsedConfig = configParser.parseConfigFile(configFilePath='test/config_parser_tests/fixtures/faulty_gpiodevices.yaml')

        assert isinstance(parsedConfig, dict)
        assert len(parsedConfig) == 1

        self.__checkResults(parsedConfig, expectedResult)

    def __checkResults(self, actual, expected):
        for currentKey in expected.keys():
            expList = expected[currentKey]
            actList = actual[currentKey]

            if currentKey == 'PowerPlugs':
                for plugs in zip(expList, actList):
                    expectedPlug = plugs[0]
                    actualPlug = plugs[1]

                    assert expectedPlug.name == actualPlug.name
                    assert expectedPlug.codes == actualPlug.codes
                    assert expectedPlug.protocol == actualPlug.protocol
                    assert expectedPlug.pulselength == actualPlug.pulselength
            
            if currentKey == 'GPIODevices':
                for gpioDev in zip(expList, actList):
                    expectedDevice = gpioDev[0]
                    actualDevice = gpioDev[1]

                    assert expectedDevice.name == actualDevice.name
                    assert expectedDevice.pin == actualDevice.pin

    def __checkResultsNew(self, actual, expected):
        orderedActual = OrderedDict(sorted(actual.items()))
        orderedExpected = OrderedDict(sorted(expected.items()))

        for (actDevKey, actDev), (expDevKey, expDev) in zip(orderedActual.items(), orderedExpected.items()):
            assert actDevKey == expDevKey
            assert actDev.name == expDev.name

            if isinstance(actDev, PowerPlug):
                assert actDev.codes == expDev.codes
                assert actDev.protocol == expDev.protocol
                assert actDev.pulselength == expDev.pulselength
            
            elif isinstance(actDev, GPIODevice):
                assert actDev.pin == expDev.pin
            
            else:
                assert False, 'Type {} should not be valid.'.format(type(actDev))
            

