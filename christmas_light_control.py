import coloredlogs
import logging
import paho.mqtt.client as mqtt
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
configParser = ConfigParser(configFilePath=args.configpath)
devDict = {}
try:
    devDict = configParser.parseConfigFile()
except FileNotFoundError:
    exit(1)
except Exception as ex:
    logger.error('Unexpected Error: {}'.format(ex))
    logger.exception(ex)
    exit(1)

def on_connect(client, userdata, flags, rc):
    logger.info('Sucessfully connected to the mqtt broker')

    logger.debug('Subscribing to root topic: {}'.format(args.topic))
    client.subscribe(args.topic)

def on_message(client, userdata, message):
    logger.debug('Received mqtt messaged from the broker')
    logger.debug('Topic: {}'.format(message.topic))
    logger.debug('Content: {}'.format(message.payload))

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

logger.info('Connecting to the MQTT Broker...')
logger.debug('MQTT Broker host: {}:{}'.format(args.host, args.port))
client.connect(args.host, port=args.port)

logger.info('Waiting for mqtt messages...')
client.loop_forever()
