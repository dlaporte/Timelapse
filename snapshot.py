#!/usr/bin/python
from datetime import datetime
import time
import os

file_prefix = "cabin-timelapse-"
pktriggercord_cli = "/usr/bin/pktriggercord-cli --model K-5 --file_format dng -m AV -i 200 -a 8"
save_location = "/root/cabin-timelapse"
dropbox_uploader = "/root/bin/dropbox_uploader.sh"
# dropbox location is relative to /Apps/cabin-timelapse
dropbox_location = "/"

filename = save_location + "/" + file_prefix + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".dng"
os.system(pktriggercord_cli + " > " + filename)
os.system(dropbox_uploader + " upload " + filename + " " + dropbox_location + " && rm -f " + filename)

