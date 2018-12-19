import coloredlogs
import logging
import paho
import argparse

from src.config_parser import ConfigParser

# Create a logger instance
logger = logging.getLogger('MainApplication')

# Create a logging instance
coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s] %(name)s %(levelname)s %(message)s'
coloredlogs.install(level='DEBUG', logger=logger)


# Register the command line arguments.
argParser = argparse.ArgumentParser(description='Simple application that listens to mqtt messages from a defined broker and toggles defined devices.')
argParser.add_argument('-t', '--topic', type=str, default='', help='Root topic, where we want to subscribe to.')
argParser.add_argument('-a', '--host', type=str, default='127.0.0.1', help='Host of the MQTT Broker to which we want so subscribe.')
argParser.add_argument('-p', '--port', type=int, default=1883, help='Port of the MQTT Broker to which we want to subscribe.')
argParser.add_argument('-c', '--configpath', type=str, default='config.yaml', help='Search path for the config file. Per default, this file is located in the applications main directory.')

# Parse the command line arguments
args = argParser.parse_args()

# Parse the config file
#configParser = ConfigParser(configFilePath=args.configpath)
#devDict = {}
#try:
#    devDict = configParser.parseConfigFile()
#except Exception as ex:


logger.debug('Debug')
logger.info('Info')
logger.warning('Warning')
logger.error('Error')
