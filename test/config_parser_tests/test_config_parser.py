import pytest
import logging

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
            'PowerPlugs': [
                PowerPlug(
                    [123, 567], name='PowerPlug1', protocol=0, pulselength=567)
                ],
            'GPIODevices': [
                GPIODevice('Switch1', 2)
            ]
        }

        parsedConfig = configParser.parseConfigFile(configFilePath='test/config_parser_tests/fixtures/everything.yaml')
        
        assert isinstance(parsedConfig, dict)
        assert len(parsedConfig) == 2
        
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

