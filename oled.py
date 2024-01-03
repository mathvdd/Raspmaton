import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

min_refresh_rate = 0.5 #in seconds

path_drive = os.path.join(os.path.expanduser('~'), 'USBdrive')

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

	try:
		with open(os.path.join(os.path.expanduser('~'), 'Raspmaton', 'status'), 'r') as file:
			status = file.read()
	except:
		status = 'error status'

	try:
		with open(os.path.join(os.path.expanduser('~'), 'Raspmaton', 'FTPstatus'), 'r') as file:
			FTPstatus = file.read()
	except:
		FTPstatus = 'error FTP status'

	try:
		with open(os.path.join(os.path.expanduser('~'), 'www', 'fold_name.conf'), 'r') as file:
			foldname = file.read()
	except:
		foldname = 'error'




	with open(os.path.join(os.path.expanduser('~'), 'www', 'fold_name.conf'), 'r') as file:
		im_folder = file.read()
	im_path = os.path.join(path_drive, im_folder)
	nim = len(os.listdir(im_path))

	draw.text((0,0), f'STA: {status}', font=font, fill=255)
	draw.text((90,0), f"| #{nim}", font=font, fill=255)
	draw.text((0,12), f'FTP: {FTPstatus}', font=font, fill=255)
	draw.text((90,12), f'| {foldname}', font=font, fill=255)
	draw.text((0,15), f"_________________________", font=font, fill=255)
	draw.text((0,27), f"Wifi:", font=font, fill=255)
	draw.text((24,27), f"{str(int(sig/0.7))}%", font=font, fill=255)
	if (tnow % 10) > 5:
		draw.text((54,27), f"{SSID}", font=font, fill=255)
	else:
		draw.text((54,27), f"{IP}", font=font, fill=255)
	#draw.text((0,40), f"IP: {IP}",  font=font, fill=255)
	draw.text((0,30), f"_________________________", font=font, fill=255)
	draw.text((0,42), f"   Temp", font=font, fill=255)
	draw.text((43,42), f"|   CPU", font=font, fill=255)
	draw.text((86,42), f"|   Mem", font=font, fill=255)
	draw.text((0,54), f"   {temp}°C", font=font, fill=255)
	draw.text((43,54), f"|   {CPU}", font=font, fill=255)
	draw.text((86,54), f"|   {str(Mem)}%", font=font, fill=255)

	# Display to screen
	disp.image(image)  # set display buffer with image buffer
	disp.display()  # write display buffer to physical display

	try:
		time.sleep(min_refresh_rate - ((time.time() - tnow)))
	except:
		pass
