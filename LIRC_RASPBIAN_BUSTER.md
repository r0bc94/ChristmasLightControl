# How To Install and Configure LIRC on Rasbian Buster

Its possible to control any arbitrary IR - Device by using lirc. 
To use this, its (obivously) necessarry to actually install and configure LIRC on
your raspberry pi. 

## LIRC on Debian Buster

Unfortionatly, there are some issue when it comes to lirc support on debian. 
This means that its not possible to simply install and use lirc from the
debian packet repository. 

* It will install just fine, but as soon as you try to set up your remote it fails. 

This seems to occour because of a bug inside the lirc implementation itself (they changed the
backing library or so). 

Long story short: You need to apply a patch from a random user and build lirc itself. 

The whole process is very well described here: https://gist.github.com/billpatrianakos/cb72e984d4730043fe79cbe5fc8f7941

## Install and configure LIRC

As I told you in the paragraph above, you need to apply a patch and rebuild lirc. Since this 
can take a fair amount of time (especially on the older raspberry pies), I've already prebuild the packages 
with the applied path. You can find the `deb` - packages inside the `lirc_patched` directory of this repository.

To actually install and configure lirc, you have to do the following steps: 

0. Remove a previously installed version of lirc: 
```
sudo apt purge lirc
```

1. Install the patched lirc version and required libraries: 

```
cd lirc_patched
sudo apt install ./liblirc0_0.10.1-5.2_armhf.deb ./liblircclient0_0.10.1-5.2_armhf.deb ./lirc_0.10.1-5.2_armhf.deb
```

2. Edit the `/etc/lirc/lirc_options.conf` file and change the following value: 

```
driver          = default
device          = /dev/lirc0
```

3. Uncomment the following values in the `/boot/config.txt` file:

```
dtoverlay=gpio-ir,gpio_pin=18
dtoverlay=gpio-ir-tx,gpio_pin=17
```
_Note: The GPIO - Pin numbers refer to the GPIO Pin numbers of the broadcom chip. For example: GPIO18 is actually pin 12 on the raspberry pi_

4. Reboot

### Test the Installation

Before we continue, we want to test the installation and look, if we can actually receive some IR - Signals from
a remote control. 

_This step can be skipped, if you only have an IR - Sender._

1. Disable the lircd - Service: 

```
sudo systemctl stop lircd
```

2. Try to receive some IR - Signals: 
```
mode2 -d /dev/lirc0
```

You can press and hold a button on your remote control. If you can see a _wall of text_
this means that your receive setup works. 

### Setup a new Remote control

To set up a new remote control, we use the `irrecord` command, provided by lirc. 

1. Make sure, that the _lircd_ service is stopped: 
```
sudo systemctl stop lircd
```

2. See, which Key - Names you can use: 
```
irrecord --list-namespace
```

3. Generate a new config file for your IR - Remote control: 
```
irrecord -d /dev/lirc1 ~/lircd.conf
```
Just follow the given steps.

4. Move the generated config to the lirc - config folder: `sudo mv test.lircd.conf /etc/lircd/lircd.conf.d
5. Start the lircd daemon: 
```
sudo systemctl start lircd
```

6. Test your configuration by sending a key from your remote control to your device. 
To send a Key, use the following command: 

```
irsend SEND_ONCE hifi KEY_POWER
```

**Sometimes its necessary to actually send the command twice in order for your device to recognize it.
In this case, try to add the `--count 2` flag to send the command twice.**
