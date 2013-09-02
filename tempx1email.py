import os
import glob
import time
import urllib
import json
import netifaces
import gdata
import gdata.spreadsheet.service as gdss
import RPi.GPIO as GPIO
import smtplib

GREEN_LED = 24
RED_LED = 23

WARN_TEMP_HIGH = 85
WARN_TEMP_LOW = 40

EMAIL_LIST = [
	'jbrodie@gmail.com',
	'scott.brodie@mssm.edu',
	'mgruen+lakehouse@gmail.com',
	'lakehousepi@gmail.com'
]

SPREADSHEET_NAME = 'LakeHouseData'
USERNAME = 'lakehousepi@gmail.com'
PASSWORD = 'lakehousepi!'

SPREADSHEETKEY = '0AjzyT7vXIZUudEo1TXNLMXRlanNRc1ZyZjFBclZkN0E'
WORKSHEETID = 'od6'

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)


def get_global_ip():
	jss = urllib.URLopener().open('http://jsonip.com').read()
	obj = json.loads(jss)
	ip = obj['ip']
	return ip

GPIO.output(GREEN_LED, True)

global_ip = get_global_ip()
local_ip = netifaces.ifaddresses("wlan0").get(netifaces.AF_INET)[0]['addr']

spr_client = gdss.SpreadsheetsService()
spr_client.email = USERNAME
spr_client.password = PASSWORD
spr_client.source = 'Example Spreadsheet Writing Application'
spr_client.ProgrammaticLogin()

gd_client = gdss.SpreadsheetsService()
gd_client.email = USERNAME
gd_client.password = PASSWORD
gd_client.ProgrammaticLogin()


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir  = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines=read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string)/1000.0
		temp_f = temp_c * 9.0/5.0 + 32.0
		return (temp_c, temp_f,)

# while True:    This loop commneted out to simply print the temperature once
#	print(read_temp())
#	time.sleep(1)

temp = read_temp()
print(temp)

if temp[1] > WARN_TEMP_HIGH or temp[1] < WARN_TEMP_LOW:
	fromaddr = USERNAME
	toaddrs = EMAIL_LIST
	if temp[1] > WARN_TEMP_HIGH:
		msg = 'Subject: The temperature is too darn high!\n\nIt is %d degrees in here!' % temp[1]
	else:
		msg = 'Subject: The temperature is too darn low!\n\nIt is %d degrees in here!' % temp[1]
	username = USERNAME
	password = PASSWORD
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username, password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

# Prepare the dictionary to write
dict = {}
dict['date'] = time.strftime('%m/%d/%Y')
dict['time'] = time.strftime('%H:%M:%S')
dict['tempcentigrade'] = str(temp[0])
dict['tempfahrenheit'] = str(temp[1])
dict['localip'] = local_ip
dict['globalip'] = global_ip

print dict

entry = spr_client.InsertRow(dict, SPREADSHEETKEY, WORKSHEETID)
if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
	print "Insert row succeeded."
else:
	print "Insert row failed."
	GPIO.output(RED_LED, True)
	time.sleep(5)
	GPIO.output(RED_LED, False)

GPIO.output(GREEN_LED, False)
