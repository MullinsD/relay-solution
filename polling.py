#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread
import urllib, urllib2
from time import gmtime, strftime
import RPi.GPIO as GPIO
import os
import mcp3008

# ===========================================================================
# Google Account Details
# ===========================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output( 23, True )
GPIO.output( 18, True )

# This is the function you care about
def checkRelay():
	# opens up the on_off_switch.php which contains the status of the relay
	response = urllib.urlopen("http://people.eecs.ku.edu/~smar/garden_pi/on_off_switch.php")
	# reads in the first line
	status = response.readline()
	# if it is on its sets the pin controlling the relay accordingly
	if 'on' in status:
		GPIO.output( 18, False )
	elif 'off' in status:
		GPIO.output( 18, True )
	# reads the second line which controls another pin on the relay
	status = response.readline()

	if 'on' in status:
		GPIO.output( 23, False )
	elif 'off' in status:
		GPIO.output( 23, True )


def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading

# ===========================================================================
# Example Code
# ===========================================================================



# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!

  output = subprocess.check_output("./loldht")
  print output
  matches = re.search("Humidity =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))
  
  # search for humidity printout
  matches = re.search("Temperature =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  temp = float(matches.group(1))
  r = RCtime(25)
  soil = mcp3008.readadc(5)

  if(r > 50):
	light = "OFF"
  else:
	light = "ON"

  rtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

  print "Temperature: %.1f C" % temp
  print "Humidity:    %.1f %%" % humidity
  print light
  print r
  print soil
  print rtime

  # this is how you can add data to a database via a python script
  mydata =[('temp', temp),('light', light),('humidity', humidity),('soil', soil),('time', rtime)]
  mydata = urllib.urlencode(mydata)
  path = 'http://people.eecs.ku.edu/~drmullin/add_data.php'
  req = urllib2.Request(path, mydata)
  req.add_header("Content-type", "application/x-www-form-urlencoded")
  page = urllib2.urlopen(req).read()
  
  checkRelay()
  
  time.sleep(2)
