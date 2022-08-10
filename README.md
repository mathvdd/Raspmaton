# Raspmaton

This concisely describe my build of a photo booth with a Raspberry Pi 4. It is there for me as notes so not always didactic and well written but could help if you are trying to do the same thing. The features of the photo booth are:

- No screen (The booth has a mirror and not a screen for people to pose)
- the shot is indicated by a led strip blinking
- a fan is added for heat removal
- the website is rather simple at the moment, but still has a lazyload feature (with lazysizes)
- the files are stored in an external USB drive
- a website with the pictures is updated through ftp (with ftplib)
- a config webpage where it will be possible to change the folder where the pictures will be stored and from which they will be displayed, without need to connect to the RPi (and also where it is possible to make an update from this repository)

The previous version was set up to work without internet and instead of the ftp uplaoad had the following features:

- pictures are available from a wifi hotspot (RaspAP) of the RPi
- the wifi hotspot has an captive portal (NoDogSplash) redirecting to the page with the pictures

The instructions are still availables at the end of the readme file but the changes to raspmaton.py may not be backward compatible (look before 23/07/2022 in the repository for the previous version that was build with those features.
One drawback I never solved: NoDogSplash does not work if the RPi is not connected to the internet, I saw discussion about this online and there may be solutions but never tried try to implement them

# Software

## Install an OS on the raspberry
https://www.raspberrypi.com/software/
Here I use RASPBERRY PI OS LITE (30-BIT) Debian Bullseye from the Raspberry Pi Imager v1.7.2.

In the advanced options:

- Enable SSH (I will use SSH to configure the Pi, alternatively connect it to a screen and keyboard)
- Set USERNAME and PASSWORD

Boot the RPi. Connect to the LAN with an ethernet cable (or can also connect to the wifi through the advanced setup of the imager). Connect to ssh

`ssh USERNAME@IP_ADRESS`

update the repository

`sudo apt update && sudo apt upgrade`

`sudo reboot` (not sure that one is useful but doesn't cost anything)

## Downloading the scripts

if git not installed:

`sudo apt install git`

`git clone https://github.com/mathvdd/Raspmaton.git` from the home directory to download all the scripts from this repository in ~/Raspmaton

`git pull` while in the directory to update it from github


## Raspmaton and generate website script

The main script to control the photobooth and generate the website is **raspmaton.py**

Make the www dir:

`cd ~/ && mkdir www`

The website uses a lazysizes (https://github.com/aFarkas/lazysizes) to lazyload the pictures. lazysizes.min.js should be put in the **~/www** directory. It can be done with:

`curl -o ~/www/lazysizes.min.js http://afarkas.github.io/lazysizes/lazysizes.min.js`

Add the following line to */etc/rc.local* just before *exit 0* for launching raspmaton.py at boot:

> sudo -u USERNAME python /home/USERNAME/Raspmaton/raspmaton.py &

## ftp credentials

The ftp credentials need to be stored the 'parameters.txt' file in the following format (see rename_parameters for the format)

## Configuration webpage

3 files need to be upladed in the remote ftp directory:

- fold_name.conf
- git_update.conf
- config.php

The first 2 will be automatically updated by config.php.

Navigate config.php to:

- change the name of the folder where the pictures will be stored/ from which the pictures will be displayed
- fetch an update from the github repository (and reboot)

So no need to go change those parameters in the code on the RPi later

## protect the webpage with a password

the webpage can be protected with a password by renaming and updating the given .htaccess and .htpasswd files, and put them on the remote ftp directory. The path to .htpasswd in .htaccess need to be an absolute path. the files holding the configuration are not protected to be easily readable by the RPi. the password can be crypted with the htpasswd utils from the appache utils library (or something like that, look it up)

`htpasswd -b -c FILE_TO_STORE_PWD USERNAME PASSWORD`

## connet to a wifi network

To see available networks:

`sudo iwlist wlan0 scan | grep ESSID`

To see current IP address:

`ifconfig`

Somehow need to set the country in the RPi wifi settings if wifi was not set up before

`sudo raspi-config` -> System options -> Wireless LAN

continue with SSID the name of the wifi network to connect to and PASSWORD

To see registered networks or manually add networks:

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

# Hardware

## Camera setup

Physically connect the Camera (Official RPi camera)

Connect the camera in the OS:

`sudo raspi-config` -> Interface Options -> Legacy camera -> Enable (-> reboot?)

Install the picamera python module:

(if not already done: `sudo apt install python3-pip`)

`pip3 install picamera`

Take a first picture to test the camera:

`python Raspmaton/cameratest.py`

## Light setup

I got a LED USB lamp made up of circular tube filled with two analog LED strips (white and warm white) and a controller (with 4 buttons for ON/OFF, intensity and color warmth) in the middle of the USB cable. I desoldered the controller from the cable to be left with the 3 wires of led strip (V+; V- white; V- warm white), in order to control the LEDs from a RPi PWM pin with a transistor. With all LEDs at max intesity (5V), the LED strip takes individually about 2A. I can get about 1A from the RPi 5V pins (whatever the state of the fan) with my power supply which is sufficient to light up the LEDs (albeit not to their max intensity). The USB ports current is not enough to light my strip however, although I read somewhere they could supply up to 1.2A.

In the end, I resoldered the LED 5V and GND to the USB connector (after removing the controller) as well as pin female connectors, to be able to choose between powering the LED strip both from the RPi and an external power supply. I used a TIP142T transistor I had on hand (maybe not the best choice, I know little about transistors).

Layout:

- RPi pin 12 (GPIO 18, PWM0) to ~670 ohm resistor to transistor base
- Transistor emitter to RPi pin 14 (GND) (AND to the external power supply GND if and external supply is used)
- Transistor collector to negative LED strip
- Positive LED strip to RPi pin 2 (5V) or external power supply

To test it is working:

`python Raspmaton/ledtest.py`

## Button setup

Added a button in a pull up circuit as an input for triggering the camera. The capacitor is added because false push are triggered when the wire moves. pull_up_down=GPIO.PUD_UP should be enough insted of a pull up resistor to 3.3V (https://github.com/raspberrypilearning/physical-computing-guide/blob/master/pull_up_down.md) but it did not show good results for me

Layout:

- First pin of the button to 1k ohm resistor to RPI pin 10 (GPIO 15)
- Second pin of the button to RPi pin 20 (GND)
- RPI pin 10 (GPIO 15) to a 10k ohm resistor to RPi pin 1 (3.3V)
- a 10 000 nanofarad capacitor between RPi pin 1 (3.3V) and the first pin of the button

pull up configuration gave better results than pull down

To test it is working:

`python Raspmaton/buttontest.py`

## External drive setup

The pictures will be stored on an external USB drive. It will be automounted in folder in ~/

Crate a folder where to mount the drive:

`mkdir USBdrive`

Once inserted find the drive location with `lsblk`

to get the UUID with `blkid`

Modify fstab with the automount rules:

`sudo cp /etc/fstab /etc/fstab.back`

`sudo nano /etc/fstab`

and add the following line (for a fat32 filesystem):

> UUID=UUID_OF_USB_DRIVE /home/USERNAME/USBdrive vfat defaults,auto,users,rw,nofail,umask=000 0 0

The drive will be mounted at each boot (reboot with 'reboot' or unplug), or with `mount -a`.

a 'this_is_the_drive' file need to be on the USB drive so the script can check it is mounted at startup. With the drive mounted:

`touch USBdrive/this_is_the_drive`

## Indicator LEDs

3 indicator leds are added:

blue LED -> 1kOhm resistor -> pin 16
green LED -> 1kOhm resistor -> pin 18
red LED -> 1kOhm resistor -> pin 22

OUT OF DATE

At startup: the blue led blink when the script start and then stay on. The green led blink twice if the USB drive is mounted. The red blink indefinitely if the USB drive is not mounted (and the rest of the script is not executed)

When the website is updated through ftp: green blink means successful, red blink means failure (but the picture will still be saved on the USB drive and uploaded at next successful update)

## Adding a fan

The fan is controlled by a python script reading the temperature sensor of the RPi and a 2N3904 NPN transistor.

Layout:

- RPi pin 4 (GND) to transistor emitter
- RPi pin 6 (GPIO 14) to 1kOhm resistor to transistor base
- Fan negative to transistor collector
- Fan positive to RPi pin 2 (5V)

The python script (fancontrol.py) is originally from here: https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python

Add the following line to */etc/rc.local* just before *exit 0* for launching fancontrol.py at boot:

> python /home/USERNAME/Raspmaton/fancontrol.py &

`sudo reboot`

### some more commands

File transfert over ssh with scp:

`scp /PATH/TO/FILE/fancontrol.py USERNAME@IP_ADRESS:fancontrol.py`

Reading the temperature of the RPi from bash:

`/usr/bin/vcgencmd measure_temp`

See if the process is active after startup:

`ps aux | grep fan`

# Local version with wifi hotspot (may not be working with the most recent version, see the repository before 23/07/2022)

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

> SplashPage raspmaton.html


Add the following line to */etc/rc.local* just before *exit 0* for launching NoDogSplash at boot:

> nodogsplash

Reboot for config changes to take effect
