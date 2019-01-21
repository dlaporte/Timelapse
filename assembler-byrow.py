#!/usr/local/bin/python3

# join the output of this script into rows using:
#
# montage 101*.jpg -mode concatenate -tile 44 cabin1.png
# montage 102*.jpg -mode concatenate -tile 44 cabin2.png
# etc...
#
# and then join those using:
#
# montage cabin*.png -mode concatenate -tile 1 cabin.png
#

import ephem
from datetime import datetime
from datetime import timedelta
#from PIL import Image
from wand.image import Image
import time
import os


#timelapse_directory = '/Users/dlaporte/Dropbox/Apps/Cabin Timelapse'
timelapse_directory = '/Users/dlaporte/Dropbox/test'
timelapse_prefix = 'cabin-timelapse-'
#timelapse_suffix = 'tiff'
timelapse_suffix = 'jpg'
final_directory = '/Users/dlaporte/Dropbox/Code/Timelapse/test-byrow'

timelapse_start = '01/17/19'
timelapse_end = '01/20/19'

start = datetime.strptime(timelapse_start, '%m/%d/%y')
end = datetime.strptime(timelapse_end, '%m/%d/%y')


days = {}
day = start
count = 0
daily_total = None
target_width = None
target_height = None

while (day <= end):

	images = []
	for file in sorted(os.listdir(timelapse_directory)):
		if file.endswith(timelapse_suffix):
			print(file)
			if file.startswith(timelapse_prefix + day.strftime('%Y-%m-%d') + '-'):
				with Image(filename=timelapse_directory + '/' + file) as img:
					if target_height is None:
						target_height = img.height
						target_width = img.width
					else:
						if target_height != img.height:
							exit(day.strftime('%Y-%m-%d') + ': mis-matched resolution (' + str(img.height) + ')')
					images.append(img.clone())

	if daily_total is None:
	    daily_total = len(images)
	else:
		if daily_total != len(images):
			exit(day.strftime('%Y-%m-%d') + ': mis-matched days (' + str(len(images)) + ')')
	days[count] = images

	day += timedelta(days=1)
	count += 1

row_height = int(target_height / count)
column_width = int(target_width / daily_total)

print("there are " + str(count) + " days")
print("there are " + str(daily_total) + " images per day")
print("row height " + str(row_height))
print("column width " + str(column_width))

x = 0
y = 0

day_num = 100
img_num = 100

for day in days:
	day_num += 1
	for img in days[day]:
		img.rotate(1.7)
		img.crop(x, y, width=column_width, height=row_height)
		file = str(day_num) + '_' + str(img_num) + '.jpg'
		img.save(filename=final_directory + '/' + file)
		img_num += 1
		x += column_width
	y += row_height
	x = 0
exit()
