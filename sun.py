#!/usr/bin/python
import ephem
import datetime

somewhere = ephem.Observer()
somewhere.lat = '42.380238'
somewhere.lon = '-71.116130'
somewhere.elevation = 56

sun     = ephem.Sun()
sunrise = ephem.localtime(somewhere.next_rising(sun))
sunset  = ephem.localtime(somewhere.next_setting(sun))

print ("Sunrise %s" % sunrise)
print ("Sunset  %s" % sunset)
