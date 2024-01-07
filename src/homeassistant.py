import logging
import json
from paho.mqtt.client import Client

from src.power_plug import PowerPlug

logger = logging.getLogger().getChild('HomeAssistant expose')

def expose_devices(devices_dict: dict, mqttclient: Client, **expose_args):
    """
    Exposes all RF - Plug Devices inside the passed devices dict to Homeassistant via 
    MQTT. 
    """

    for key, val in devices_dict.items():
        # Only expose PowerPlugs for now.
        if not isinstance(val, PowerPlug):
            logger.debug(f'Skipping non PowerPlug Device: {key}')
            continue

        # Serialize and Publish Switch Data for HomeAssistant
        hadict = create_ha_dict(key, val, expose_args['root_topic'])
        hadict_serialized = json.dumps(hadict)

        ha_device_config_topic = f'{expose_args["discovery_topic"]}/switch/{key}/config'

        logger.debug(f'Publishing HomeAssistant Discovery Data for Device: {key}')
        logger.debug(f'topic: {ha_device_config_topic}; Payload: {hadict_serialized}')
        mqttclient.publish(ha_device_config_topic, hadict_serialized)


def create_ha_dict(devname: str, devobject: PowerPlug, roottopic: str):
    command_topic = f'{roottopic}/{devname}' if roottopic != '#' else devname
    hadict = {
        'name': 'Switch',
        'unique_id': f'rfswitch_{devname}',
        'device': {
            'name': devobject.friendlyName,
            'identifiers': devname,
            'model': 'RFSwitch'
        },
        'command_topic': command_topic,
        'payload_on': 'ON',
        'payload_off': 'OFF',
        'retain': 'false'
    }

    return hadict
