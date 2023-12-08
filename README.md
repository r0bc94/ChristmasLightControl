# Christmas Light Control

This is a simple program for a Rasperry Pi which listens for MQTT - Messages and switches devices such as 433MHz RF Power Plugs and simple 
devices attached to any GPIO Pins on and of. This tool can also be used to control infrared devices from MQTT messages.

Originally, I made this tool to control my christmas lights, which where attached to some cheap 433MHz Power Plugs, using Homeassistant.

## How it works

At startup, this program will attached to a given MQTT broker and listens for messages on a configured topic. Each message would map to a preconfigured device, whose name should be the last portion of the received messages topic. According to the messages content, the matching device will be turned `ON` or `OFF`. 

For example, when receiving the following message: 

```
topic: /lamps/mylamp
payload: "ON"
```

The device called `mylamp` will be turned on.

### 433MHz Transmitters

To switch 433 MHz RF Power Plugs, a generic 433MHz transmitter is needed. You can still get those little circuit boards fairly cheap from Ebay, Aliexpress, Amazon and so on. 

You can find out how to attach such transmitter by having a look at the documentation of the RPI-RF python library, as this tool
also uses it: 
https://github.com/milaq/rpi-rf

One thing to mention is that this library can leverage the Enable (EN) - pin of those transmitters (if present). This means that before each transmission, a given GPIO Pin is pulled `HIGH` before and `LOW` after the transmission. This can be handy since I found
out that always running the cheapo transmitter board will jam the whole 433MHz band in a certain area around the transmitter.

In some cases however, the EN (Enable) - Pin of those transmitter boards will not be connected, and/or always pulled `HIGH` implicitly. As this was the case on my transmitter board, I simply added a small transistor between ground and the GND - Pin.
This way, the transmitter will only be active when something needs to be transmitted.


## Installation

Currently, the only way to use this this tool is to clone this repository, install the dependencies using Pipenv and starting the program in the installed python environment. 

Basically, after cloning the repository, you have to take the following steps: 
1. Make sure `pipenv` is installed. If not, you can install it with the following command: 
  ```bash
  pip install pipenv && source ~/.bashrc
  ```
2. Creating the virtual environment and installing all the needed dependencies
    ```bash
    pipenv install
    ```
3. Entering the virtual environment and running the startup script: 
    ```bash
    pipenv shell
    python christmas_light_control.py --help
    ```

## Configuration

There are two files which needs to be configured in order to use this tool.

The first file called `config.conf` contains the global configuration. There are only two options which you can set here: 

**`rf_gpio_pin`**
* Sets the GPIO Pin, where the 433 MHz RF sender is attached to. _Keep in mind that the BCM - Pin layout is used!_

**`rf_enable_pin`**
* Sets the GPIO Pin which should be pulled High before starting a transmission.

### Configure Devices

The second file is called `devices.yaml`. Here you can configure your devices and such parameters such as RF Codes. 
Basically, the file looks like so: 

```yaml
device_key:
  type: <DeviceType>
  <Device Options>
  ...
```

To add for example a RF Power Plug, you need to add the following to your `devices.yaml` - File: 
```yaml
MyLamp:
  type: "PowerPlug"
  codes:
    - <ON_CODE> 
    - <OFF_CODE>
  pulselength: 511
  protocol: 5
```

When now receiving a message on the topic `/MyLamp` with a message such as `ON`, the lamp MyLamp will be turned on. 
