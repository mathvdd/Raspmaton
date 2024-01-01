import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import subprocess

min_refresh_rate = 0.5 #in seconds

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

disp.begin() # initiate graphic library
disp.clear() # clear display
disp.display() #write display buffer to physical display

width = disp.width
height = disp.height
image = Image.new('1', (width, height)) # create blanck image. 1 for 1-bit color
draw = ImageDraw.Draw(image) #create drawing object
font = ImageFont.load_default()  # load and set default font

tstart = time.time()

while True:
	tnow = time.time()
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	cmd = "iwconfig wlan0 | grep ESSID | awk -F'\"' '{print $2}'"
	SSID = subprocess.check_output(cmd, shell=True).decode().strip('\n')

	cmd = "iwconfig wlan0 | grep Quality | awk -F'=' '{print $2}'| awk -F'/70' '{print $1}'"
	try:
		sig = int(subprocess.check_output(cmd, shell=True).decode().strip('\n'))
	except:
		sig = 0

	cmd = "hostname -I | cut -d\' \' -f1"
	IP = subprocess.check_output(cmd, shell = True ).decode().strip('\n')

	cmd = "uptime | awk '{print $(NF-2)}'"
	CPU = subprocess.check_output(cmd, shell = True ).decode().strip(',\n')
	cmd = "free -m | awk 'NR==2{print $3*100/$2}'"
	Mem = int(float(subprocess.check_output(cmd, shell = True ).decode().strip('\n')))
	cmd = "/usr/bin/vcgencmd measure_temp | awk -F \"[=']\" '{print($2)}'"
	temp = subprocess.check_output(cmd, shell=True).decode().strip('\n').split('.')[0]

    with open(os.path.join(os.path.expanduser('~'), 'Raspmaton', 'status'), 'r') as file:
        status = file.read()

	draw.text((0,0), status, font=font, fill=255)
	draw.text((0,50), str(round(tnow-tstart,2)), font=font, fill=255)
	draw.text((0,12), f"Wifi: {str(int(sig/0.7))}% {SSID}", font=font, fill=255)
	draw.text((0,22), f"IP: {IP}",  font=font, fill=255)
	draw.text((0,34), f"T:{temp}°C CPU:{CPU} Mem:{str(Mem)}%", font=font, fill=255)

	# Display to screen
	disp.image(image)  # set display buffer with image buffer
	disp.display()  # write display buffer to physical display

	try:
		time.sleep(min_refresh_rate - ((time.time() - tnow)))
	except:
		pass
