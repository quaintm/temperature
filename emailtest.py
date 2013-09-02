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
#	'jbrodie@gmail.com',
	'scott.brodie@mssm.edu',
#	'mgruen+lakehouse@gmail.com',
#	'lakehousepi@gmail.com'
]


USERNAME = 'lakehousepi@gmail.com'
PASSWORD = 'lakehousepi!'






def get_global_ip():
	jss = urllib.URLopener().open('http://jsonip.com').read()
	obj = json.loads(jss)
	ip = obj['ip']
	return ip


global_ip = get_global_ip()
local_ip = netifaces.ifaddresses("wlan0").get(netifaces.AF_INET)[0]['addr']




if True:
	fromaddr = USERNAME
	toaddrs = EMAIL_LIST
#	if temp[1] > WARN_TEMP_HIGH:
#		msg = 'Subject: The temperature is too darn high!\n\nIt is %d degrees in here!' % temp[1]
#	else:
#		msg = 'Subject: The temperature is too darn low!\n\nIt is %d degrees in here!' % temp[1]
	username = USERNAME
	password = PASSWORD
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username, password)
	server.sendmail(fromaddr, toaddrs, 'Foo')
	server.quit()

# Prepare the dictionary to write
#dict = {}
#dict['date'] = time.strftime('%m/%d/%Y')
#dict['time'] = time.strftime('%H:%M:%S')
#dict['tempcentigrade'] = str(temp[0])
#$dict['tempfahrenheit'] = str(temp[1])
#dict['localip'] = local_ip
#dict['globalip'] = global_ip

print 'Foo'
