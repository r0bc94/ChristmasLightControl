#!/usr/bin/env python3
import coloredlogs
import logging
import paho.mqtt.client as mqtt
import argparse

import RPi.GPIO as GPIO

from src.devices_parser import DevicesParser

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
argParser.add_argument('-dev', '--devicespath', type=str, default='devices.yaml', help='Search path for the devices file. Per default, this file is located in the applications main directory.')
argParser.add_argument('-e', '--enable_pin', type=int, nargs=1)

# Parse the command line arguments
args = argParser.parse_args()

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

# Initialize the GPIO pins
GPIO.setmode(GPIO.BCM)

if args.enable_pin:
    pin = args.enable_pin[0]
    logger.info(f'Enable Pin for the RF - Devices was set to pin {pin}')
    logger.debug(f'Setting pin {pin} as OUTPUT')
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    logger.info('Sucessfully connected to the mqtt broker')

    logger.debug('Subscribing to root topic: {}'.format(args.topic + '#'))
    client.subscribe(args.topic + '#')

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
    logger.debug('Cleaning up GPIO Channels')
    
    # TODO: I need some sort of cleanup function in the device classes.
    GPIO.cleanup()
