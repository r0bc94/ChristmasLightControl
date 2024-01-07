#!/usr/bin/env python3
import coloredlogs
import logging
import paho.mqtt.client as mqtt
import configargparse

try:
    import RPi.GPIO
except (RuntimeError, ModuleNotFoundError):
    print('Using Fake RPi GPIO Imports')
    from fake_rpigpio import utils, RPi
    import sys
    utils.install()
    sys.modules['RPi'] = RPi

from src.devices_parser import DevicesParser
from src.ir_device import IRDevice
from src.homeassistant import expose_devices

# Create the logger
logger = logging.getLogger()
coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s] %(name)s %(levelname)s %(message)s'
coloredlogs.install(level=logging.DEBUG, logger=logger)

# Register the command line arguments.
argParser = configargparse.ArgParser(default_config_files=['config.conf'], description='Simple application that listens to mqtt messages from a defined broker and toggles defined devices.')
argParser.add('-c', '--my-config', required=False, is_config_file=True, help='Path to a config file which should be used instead.')
argParser.add_argument('-dev', '--devicespath', type=str, default='devices.yaml', help='Search path for the devices file. Per default, this file is located in the applications main directory.')
argParser.add_argument('-d', '--debug', default=False, action='store_true', help='Log various debug informations. The log output might be a bit spammy.')

mqttConfig = argParser.add_argument_group('MQTT')

mqttConfig.add_argument('-t', '--topic', type=str, default='', help='Root topic, where we want to subscribe to.')
mqttConfig.add_argument('-a', '--host', type=str, default='127.0.0.1', help='Host of the MQTT Broker to which we want so subscribe.')
mqttConfig.add_argument('-p', '--port', type=int, default=1883, help='Port of the MQTT Broker to which we want to subscribe.')

rfDeviceConfig = argParser.add_argument_group('RF Device')
rfDeviceConfig.add_argument('--rf_gpio_pin', help='The pin where the RF - Transmitter is connected to', type=int, default=17)
rfDeviceConfig.add_argument('-e', '--rf_enable_pin', help='If your Transmitter has an optional enable pin, this needs to be set', type=int, nargs=1)

homeassistantConfig = argParser.add_argument_group('HomeAssistant', description='Arguments used to configure the connection to homeassistant')
homeassistantConfig.add_argument('--expose_to_homeassistant', default=False, action='store_true', help='If set, all devices read from the devices.yaml file will be exposed to homeassistant via the configured MQTT broker.')
homeassistantConfig.add_argument('--discovery_topic', type=str, default='homeassistant', help='Root Topic name for the homeassistant discovery. Set if it needs to be changed.')

# Parse the command line arguments
args = argParser.parse_args()
if not args.debug:
    logger.setLevel(logging.INFO)
else:
    logger.debug('Debug logging activated')

# Parse the devices file
devicesParser = DevicesParser(devicesFilePath=args.devicespath)
devDict = {}
try:
    devDict = devicesParser.parseDevicesFile(args)
except FileNotFoundError:
    exit(1)
except Exception as ex:
    logger.error('Unexpected Error: {}'.format(ex))
    logger.exception(ex)
    exit(1)

# Initialize the RPi.GPIO pins
RPi.GPIO.setmode(RPi.GPIO.BCM)

if args.rf_enable_pin:
    pin = args.rf_enable_pin[0]
    logger.info(f'Enable Pin for the RF - Devices was set to pin {pin}')
    logger.debug(f'Setting pin {pin} as OUTPUT')
    RPi.GPIO.setup(pin, RPi.GPIO.OUT)
    RPi.GPIO.output(pin, RPi.GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    logger.info('Sucessfully connected to the mqtt broker')
    topic = args.topic + '#' if args.topic[-1] == '/' else f'{args.topic}/#'

    logger.debug(f'Subscribing to root topic: {topic}')
    client.subscribe(topic)

    if args.expose_to_homeassistant: 
        logger.info('Exposing all PowerPlug Devices to Homeassistant')
        expose_devices(devDict, client, root_topic=args.topic, discovery_topic=args.discovery_topic)

def on_message(client, userdata, message):
    logger.debug('Received mqtt messaged from the broker')
    logger.debug('Topic: {}'.format(message.topic))
    logger.debug('Content: {}'.format(message.payload))

    devName = message.topic.split('/')[-1]
    
    if devName not in devDict:
        logger.warning('Device with name {} not registered.'.format(devName))
        return

    devToToggle = devDict[devName]

    messagePayload = message.payload.decode('utf-8', errors='ignore')
    if messagePayload.upper() == 'ON':
        devToToggle.turnOn()
    elif messagePayload.upper() == 'OFF':
        devToToggle.turnOff()
    elif isinstance(devToToggle, IRDevice):
        devToToggle.sendKey(messagePayload.upper())
    else:
        logger.warning('Invalid message content: {}'.format(messagePayload))

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

logger.info('Connecting to the MQTT Broker...')
logger.debug('MQTT Broker host: {}:{}'.format(args.host, args.port))
client.connect(args.host, port=args.port)

try:
    logger.info('Waiting for mqtt messages...')
    client.loop_forever()
except KeyboardInterrupt:
    logger.info('exiting...')
except Exception as ex:
    logger.error('An unexpected error occured: {}'.format(ex))
    logger.exception(ex)
finally:
    logger.debug('Cleaning up RPi.GPIO Channels')
    RPi.GPIO.cleanup()
