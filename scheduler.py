#!/usr/bin/python
import ephem
from datetime import datetime
from datetime import timedelta
import time
import os

day_shots = 30
dawn_shots = 7
twilight_shots = 7

snapshot_script = "/root/Timelapse/snapshot.py"

# cabin location and elevation
cabin = ephem.Observer()
cabin.lat = '42.380238'
cabin.lon = '-71.116130'
cabin.elevation = 56

# set time to midnight today
cabin.date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# determine interval for snapshot_interval photos per day
sun     = ephem.Sun()

sunrise = ephem.localtime(cabin.next_rising(sun))
sunset  = ephem.localtime(cabin.next_setting(sun))
sunnoon = ephem.localtime(cabin.next_transit(sun))

cabin.horizon = '-10'
dawn = ephem.localtime(cabin.next_rising(sun, use_center=True))
twilight = ephem.localtime(cabin.next_setting(sun, use_center=True))

# clear out all previous at jobs
os.system('atrm $(atq | cut -f1) > /dev/null 2>&1')

# schedule at jobs for each snapshot

# schedule dawn shots
dawn_interval =  (sunrise - dawn) / dawn_shots
time = dawn
for shot in range(dawn_shots):
        if (time > datetime.now()):
		os.system("echo " + snapshot_script + " | at -t " + time.strftime("%y%m%d%H%M"))
	time += dawn_interval

# schedule normal shots
day_interval = (sunset-sunrise) / day_shots
time = sunrise
for shot in range(day_shots):
        if (time > datetime.now()):
		os.system("echo " + snapshot_script + " | at -t " + time.strftime("%y%m%d%H%M"))
	time += day_interval

# schedule twilight shots
twilight_interval =  (twilight - sunset) / twilight_shots
time = sunset
for shot in range(twilight_shots):
        if (time > datetime.now()):
		os.system("echo " + snapshot_script + " | at -t " + time.strftime("%y%m%d%H%M"))
	time += twilight_interval
