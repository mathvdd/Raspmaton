# Raspmaton
## Install an OS on the raspberry
https://www.raspberrypi.com/software/
Here I use RASPBERRY PI OS LITE (30-BIT) Debian Bullseye from the Raspberry Pi Imager v1.7.2.

In the advanced options:

- Enable SSH (I will use SSH to configure the Pi, alternatively connect it to a screen and keyboard)
- Set USERNAME and PASSWORD

Boot the RPi. Connect to the LAN with an ethernet cable. Connect to ssh

`ssh USERNAME@IP_ADRESS`

update the repository

`sudo apt update && sudo apt upgrade`

`sudo reboot` (not sure that one is useful but doesn't cost anything)

## Installing RaspAP for wifi hotspot

https://raspap.com/

Somehow need to set the country in the RPi wifi settings (setting a SSID is not necessary, can just cancel this step)

`sudo raspi-config` -> System options -> Wireless LAN

Install RaspAP with default configuration:

`curl -sL https://install.raspap.com | bash`

After reboot of the RPi can connect to the 'raspi-webgui' network.
Browse 10.3.141.1 for settings (login: admin; pwd: secret)

- Hotspot -> Basic -> SSID: name of the wifi network
- Hotspot -> Security -> Security type: None
- **Is the QR code there to connect to the wifi?**
- Authentication: change the admin password

## Installing the captive portal (NoDogSplash)

https://nodogsplashdocs.readthedocs.io/en/stable/

`sudo apt install git libmicrohttpd-dev`

`git clone https://github.com/nodogsplash/nodogsplash.git`

`cd nodogsplash`

`make`

`sudo make install`

### Parametring NoDogSplash
(https://www.maketecheasier.com/turn-raspberry-pi-captive-portal-wi%E2%80%90fi-access-point/)

Add parameters at the end of */etc/nodogsplash/nodogsplash.conf*. The two last lines link to the future website.

> GatewayInterface wlan0

> GatewayAddress 10.3.141.1

> MaxClients 250

> AuthIdleTimeout 480

> WebRoot /home/USERNAME/www

> SplashPage photomaton.html


Add the following line to */etc/rc.local* just before *exit 0* for booting NoDogSplash at launch:

> nodogsplash

Reboot for config changes to take effect

## Camera setup

Physically connect the Camera (Official RPi camera)

Install the picamera python module:

`sudo apt install python3-pip`

`pip3 install picamera`

## Light setup

## External drive setup

## Photomaton script

## Adding a fan

The fan is controlled by a python script reading the temperature sensor of the RPi and a 2N3904 NPN transistor.

Layout:

- RPi pin 4 (GND) to transistor emitter
- RPi pin 6 (GPIO 14) to transistor base
- Fan negative to transistor collector
- Fan positive to RPi pin 2 (5V)

The python script (fancontrol.py) is originally from here: https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python

Add the following line to */etc/rc.local* just before *exit 0* for booting fancontrol.py at launch:

> python /home/USERNAME/fancontrol.py &

`sudo reboot`

### some more commands

File transfert over ssh with scp:

`scp /PATH/TO/FILE/fancontrol.py USERNAME@IP_ADRESS:fancontrol.py`

Reading the temperature of the RPi from bash:

`/usr/bin/vcgencmd measure_temp`

See if the process is active after startup:

`ps aux | grep fan`
