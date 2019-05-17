#!/usr/local/bin/python3

import ephem
from datetime import datetime
from datetime import timedelta
from PIL import Image
import time
import os


#timelapse_directory = '/Users/dlaporte/Dropbox/Apps/Cabin Timelapse'
timelapse_directory = '/Users/dlaporte/Desktop/test'
timelapse_prefix = 'cabin-timelapse-'
#timelapse_suffix = 'tiff'
timelapse_suffix = 'jpg'

timelapse_start = '01/17/19'
timelapse_end = '01/17/19'

start = datetime.strptime(timelapse_start, '%m/%d/%y')
end = datetime.strptime(timelapse_end, '%m/%d/%y')

days = {}
day = start
count = 0
daily_total = None
target_width = None
target_height = None

while (day <= end):

	files = []
	for file in os.listdir(timelapse_directory):
		if file.endswith(timelapse_suffix):
			if file.startswith(timelapse_prefix + day.strftime('%Y-%m-%d') + '-'):
				files.append(file)
				im = Image.open(timelapse_directory + '/' + file)


				if target_height is None:
				    target_height = im.size[1]
				    target_width = im.size[0]
				else:
					if target_height != im.size[1]:
						exit(day.strftime('%Y-%m-%d') + ': mis-matched resolution (' + str(len(im.size[0])) + ')')

	if daily_total is None:
	    daily_total = len(files)
	else:
		if daily_total != len(files):
			exit(day.strftime('%Y-%m-%d') + ': mis-matched days (' + str(len(files)) + ')')
	files.sort()
	days[count] = files

	day += timedelta(days=1)
	count += 1

row_height = int(target_height / daily_total)
column_width = int(target_width / count)

print("there are " + str(count) + " days")
print("there are " + str(daily_total) + " images per day")
print("row height " + str(row_height))
print("column width " + str(column_width))


x = 0
y = 0
for row in days:
	x += row_height
	for column in days[row]:
		y += column_width
		print(x)
		print(y)
		print(column)


exit()



