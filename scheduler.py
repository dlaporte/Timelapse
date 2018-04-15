#!/usr/bin/python
import ephem
from datetime import datetime
import time
import os

snapshot_interval = 30
snapshot_script = "/root/Timelapse/snapshot.py"

# cabin location and elevation
somewhere = ephem.Observer()
somewhere.lat = '42.380238'
somewhere.lon = '-71.116130'
somewhere.elevation = 56

# clear out all previous at jobs
os.system('atrm $(atq | cut -f1)')

# determine interval for snapshot_interval photos per day
sun     = ephem.Sun()
if ephem.localtime(somewhere.next_rising(sun)) < datetime.now():
	sunrise = ephem.localtime(somewhere.next_rising(sun))
else:
	sunrise = ephem.localtime(somewhere.previous_rising(sun))
sunset  = ephem.localtime(somewhere.next_setting(sun))

interval = (sunset-sunrise) / 30

# schedule at jobs for each snapshot
time = sunrise - interval
while time <= (sunset + interval):
	os.system("echo " + snapshot_script + " | at -t " + time.strftime("%y%m%d%H%M"))
	time += interval
