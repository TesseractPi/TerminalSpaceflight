#!/usr/bin/env python3

################## BASHFLIGHT ##################
### Gets latest launch and prints it to bash ###
############# Made by Sam Rohrbach #############

import logging
import sys
import signal
import requests
import json
import os
from datetime import datetime, timedelta


filepath = '/tmp/nextlaunch.json'
#url = 'https://api.spacexdata.com/v4/launches/next' # placeholder please delete
url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&mode=list&offset=2" # launchlibrary2 2.3, only the next launch in list

with open(filepath, "r") as fileThing:
	manifest = json.load(fileThing)
#print(manifest) # debug, keep commented plz :)

def signal_handler(sig, frame):
  # Handle termination signals gracefully.
  logger.info("Received signal to stop, exiting")
  sys.stdout("Received signal to stop, exiting")
  sys.stdout.write("\n")
  sys.stdout.flush()
  sys.exit(0)

# Register signal handlers for termination
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def fetch_json(url): # get json from url
    response = requests.get(url)
    response.raise_for_status()  # raise an HTTPError on a bad status
    return response.json()

def save_json(data, filepath): # save to file
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def get_last_modified_date(filepath): # find when file last modified
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp)

def get_json_value(data, key): # get value from json
	return data.get(key, "Key not found")

# Check the file's last modified date
def overwrite():
	try:
		if os.path.exists(filepath):
			last_modified_date = get_last_modified_date(filepath)
			time_difference = datetime.now() - last_modified_date
			if time_difference < timedelta(minutes=10):
				return "File modified less than 10 minutes ago"
				#print(f"File was modified less than 10 minutes ago at {last_modified_date}. Not overwriting.")
			else:
				json_data = fetch_json(url)
				save_json(json_data, filepath)
				#print(f"JSON data saved to {filepath}")
				#print(f"Last modified: {get_last_modified_date(filepath)}")
		else:
			json_data = fetch_json(url)
			save_json(json_data, filepath)
			#print(f"JSON data saved to {filepath}")
			#print(f"Last modified: {get_last_modified_date(filepath)}")
	except Exception as e:
		print(f"An error occurred: {e}")

def main():
	overwrite()
		
	if isinstance(manifest, dict):
		mission = manifest.get('name')#, "Key not found")
		#mission = get_json_value(manifest, 'name')
		net = get_json_value(manifest, 'net')
		if mission == "Key not found" or net == "Key not found":
			print(f":(")
			print(f"Your computer didn't run into a problem and doesn't need to restart. We didn't collect anything and we won't restart for you. ")
			print(f"Stop code: KEY_NOT_FOUND")
			return ":("
		print(f"Next launch: {mission} at {net}")
	else:
		return(manifest)

if __name__ == "__main__":
	main()
