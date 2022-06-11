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

Connect the camera in the OS:

`sudo raspi-config` -> Interface Options -> Legacy camera -> Enable (-> reboot?)

Install the picamera python module:

`sudo apt install python3-pip`

`pip3 install picamera`

Take a first picture to test the camera:

`python camera_test.py`

## Light setup

I got a LED USB lamp made up of circular tube filled with two analog LED strips (white and warm white) and a controller (with 4 buttons for ON/OFF, intensity and color warmth) in the middle of the USB cable. I desoldered the controller from the cable to be left with the 3 wires of led strip (V+; V- white; V- warm white), in order to control the LEDs from a RPi PWM pin with a transistor. With all LEDs at max intesity (5V), the LED strip takes individually about 2A. I can get about 1A from the RPi 5V pins (whatever the state of the fan) with my power supply which is sufficient to light up the LEDs (albeit not to their max intensity). The USB ports current is not enough to light my strip however, although I read somewhere they could supply up to 1.2A.

In the end, I resoldered the LED 5V and GND to the USB connector (after removing the controller) as well as pin female connectors, to be able to choose between powering the LED strip both from the RPi and an external power supply. I used a TIP142T transistor I had on hand (maybe not the best choice, I know little about transistors).

Layout:

- RPi pin 12 (GPIO 18, PWM0) to ~670 ohm resistor to transistor base
- Transistor emitter to RPi pin 14 (GND) (AND to the external power supply GND if and external supply is used)
- Transistor collector to negative LED strip
- Positive LED strip to RPi pin 2 (5V) or external power supply

To test it is working:

`python led_test.py`

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
