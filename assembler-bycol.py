#!/usr/local/bin/python3

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
final_filename = 'cabin_montage.jpg'

timelapse_start = '01/17/19'
timelapse_end = '01/19/19'

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
						with Image(width=target_width, height=target_height) as final_image:
							img.save(filename=final_filename)
						#print(str(target_width) + ',' + str(target_height))
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

row_height = int(target_height / daily_total)
column_width = int(target_width / count)

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
		#print(str(y) + ',' + str(x) + ' | ' + str(y + column_width) + ',' + str(x + row_height))
		img.crop(x, y, width=column_width, height=row_height)
		y += row_height
		#print(img.size)
		file = str(day_num) + '_' + str(img_num) + '.jpg'
		img.save(filename=file)
		img_num += 1

	y = 0
	x += column_width

exit()
