#!/usr/bin/env python3

############# TERMINAL SPACEFLIGHT #############
### Gets latest launch and prints it to bash ###
############# Made by Sam Rohrbach #############

import sys
import signal
import requests
import json
import os
from datetime import *

badVal = "{'name':'no','net':'whenever'}" # something is better than nothing
tmpFile = '/tmp/nextlaunch.json' # change to whatever windows temp dir if on windows
url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&mode=list&offset=2" # launchlibrary2 2.3, only the next launch in list

def signal_handler(sig, frame): # handle termination well
	logger.info("Received signal to stop, exiting")
	sys.stdout("Received signal to stop, exiting")
	sys.stdout.write("\n")
	sys.stdout.flush()
	sys.exit(0)

# signal handlers for termination
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def fetchJSON(url): # get json from url
	response = requests.get(url)
	response.raise_for_status() # raise an HTTPError on a bad status
	return response.json()

def saveJSON(data, tmpFile): # save to file
	with open(tmpFile, 'w') as file:
		json.dump(data, file, indent=4)

def whenLastModified(tmpFile): # find when file last modified
	timestamp = os.path.getmtime(tmpFile)
	return datetime.fromtimestamp(timestamp)

def main():
	manifest = "" # make sure it exists first
	# does file exist?
	try:
		if os.path.exists(tmpFile):
			#print(f"File already exists at {tmpFile}")
			lastModifiedDate = whenLastModified(tmpFile)
			timeDifference = datetime.now() - lastModifiedDate
			if manifest == badVal or manifest == "":
				jsonData = fetchJSON(url)
				saveJSON(jsonData, tmpFile)
				#print(f"JSON data saved to {tmpFile}")
				#print(f"Last modified: {whenLastModified(tmpFile)}")		
			if (timeDifference < timedelta(minutes=10)):
				#print(f"Cache was modified recently at {lastModifiedDate}, skipping overwrite")
				whatever = "blah blah placeholder"
			else:
				jsonData = fetchJSON(url)
				saveJSON(jsonData, tmpFile)
				#print(f"JSON data saved to {tmpFile}")
				#print(f"Last modified: {whenLastModified(tmpFile)}")
		else:
			fileThing = open(tmpFile, "w")
			fileThing.write(badVal)
			print(f"Cache does not exist at {tmpFile}, creating one")
			with open(tmpFile, "r") as fileThing:
				manifest = fileThing.read()
			jsonData = fetchJSON(url)
			saveJSON(jsonData, tmpFile)
			#print(f"JSON data saved to {tmpFile}")
			#print(f"Last modified: {whenLastModified(tmpFile)}")
	except FileNotFoundError:
		fileThing = open(tmpFile, "w")
		fileThing.write(badVal)
		print(f"Cache does not exist at {tmpFile}, creating one")
		with open(tmpFile, "r") as fileThing:
			manifest = fileThing.read()
		jsonData = fetchJSON(url)
		saveJSON(jsonData, tmpFile)
		#print(f"JSON data saved to {tmpFile}")
	
	with open(tmpFile, "r") as fileThing:
		manifest = fileThing.read()

	# get actual data
	wholeThing = json.loads(manifest)
	mission = wholeThing["results"][0]["name"]
	net = wholeThing["results"][0]["net"]
	return(f"Next launch: {str(mission)} | {str(net)}")
	#return results

print(f"{main()}") # FINALLY!!!!!1
