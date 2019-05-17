#!/usr/bin/python
from datetime import datetime
import time
import os

file_prefix = "cabin-timelapse-"
pktriggercord_cli = "/usr/bin/pktriggercord-cli --model K-5 --file_format dng -m AV -i 100 -a 11 --ae_metering="
save_location = "/root/cabin-timelapse"
dropbox_uploader = "/root/bin/dropbox_uploader.sh"

# dropbox location is relative to "/Apps/Cabin Timelapse"
dropbox_subdir = datetime.now().strftime("%Y-%m-%d")

dropbox_location = dropbox_subdir

# create directory for snapshots
os.system(dropbox_uploader + " mkdir " + dropbox_location)

filename = save_location + "/" + file_prefix + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".dng"
os.system(pktriggercord_cli + " > " + filename)
os.system(dropbox_uploader + " upload " + filename + " " + dropbox_location + " && rm -f " + filename)
