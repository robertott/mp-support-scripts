"""Imports Segment.com-formattted data to a Segment.com project, 
which can subsequently pipe the imported data into Mixpanel.

Be sure to 'pip install mixpanel-py' in your terminal before running 
this script, as it relies on the Mixpanel Python library to complete
the 'resurface' step at the end.

This version still needs to be 'genericized'.
"""
import json
import requests
import os
from mixpanel import Mixpanel

folder_name = "files"
write_key = raw_input("Please enter Segment write key:  ") 
token = raw_input("Please enter Mixpanel project token:  ")

mp = Mixpanel(token)

headers = {'content-type': 'application/json'}

counter = 0
eventsToResurface = set()

for importFile in os.listdir(folder_name):
	if os.path.getsize(folder_name+"/"+importFile) == 0:
		continue
	print importFile
	f = open(folder_name+"/"+importFile, "rU")
	data = f.read()
	data = json.loads(data)
	del data["integrations"]
	del data["options"]["providers"]
	payload = {}
	payload["batch"] = []
	payload["batch"].append(data)
	try:
		eventsToResurface.add(data["event"])
	except:
		pass
	payload = json.dumps(payload)

	counter += 1
	print "Importing %d of %d (%s)" % (counter, len(os.listdir(folder_name)), importFile)
	r = requests.post("https://api.segment.io/v1/import", data=payload, headers=headers, auth=(write_key, ''))
	print r.status_code
	print r.content

decision = raw_input("Resurface these events in the project? (Y/N) (This WILL send actual events to your project!)  ")

if "y" in decision or "Y" in decision:
	for item in eventsToResurface:
		mp.track("test", item)
		print "resurfacing " + item
	print "done!"

