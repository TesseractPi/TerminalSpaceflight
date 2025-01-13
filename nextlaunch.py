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

badVal = "{'name':'no','net':'whenever'}"
tmpFile = '/tmp/nextlaunch.json'
url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&mode=list&offset=2" # launchlibrary2 2.3, only the next launch in list
manifest = ""

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
    response.raise_for_status()  # raise an HTTPError on a bad status
    return response.json()

def saveJSON(data, tmpFile): # save to file
    with open(tmpFile, 'w') as file:
        json.dump(data, file, indent=4)

def whenLastModified(tmpFile): # find when file last modified
    timestamp = os.path.getmtime(tmpFile)
    return datetime.fromtimestamp(timestamp)

def getJSONValue(data, key): # get value from json
	data2 = json.loads(data)
	return data2[key]

def main():
	global manifest
	# does file exist?
	try:
		if os.path.exists(tmpFile):
			print(f"File already exists")
		else:
			fileThing = open(tmpFile, "w")
			fileThing.write(badVal)
			print(f"Created file at {tmpFile} with contents {badVal}")
			with open(tmpFile, "r") as fileThing:
				manifest = fileThing.read()
	except FileNotFoundError:
		fileThing = open(tmpFile, "w")
		fileThing.write(badVal)
		print(f"Created file at {tmpFile} with contents {badVal}")
		with open(tmpFile, "r") as fileThing:
			manifest = fileThing.read()
	
	print(f"manifest is {manifest}")

	# when file last modified?
	try:
		if os.path.exists(tmpFile):
			lastModifiedDate = whenLastModified(tmpFile)
			timeDifference = datetime.now() - lastModifiedDate
			if timeDifference < timedelta(minutes=10) and manifest != badVal:
				#return "File modified less than 10 minutes ago"
				print(f"File was modified less than 10 minutes ago at {lastModifiedDate}. Not overwriting.")
			else:
				jsonData = fetchJSON(url)
				saveJSON(jsonData, tmpFile)
				print(f"JSON data saved to {tmpFile}")
				print(f"Last modified: {whenLastModified(tmpFile)}")
		else:
			jsonData = fetchJSON(url)
			saveJSON(jsonData, tmpFile)
			print(f"JSON data saved to {tmpFile}")
			print(f"Last modified: {whenLastModified(tmpFile)}")
	except TypeError: #Exception as e:
		print(f"kndskhdsfjhfdjkd")
		#print(f"An error occurred: {e}")
	
	# get actual data
	mission = getJSONValue(manifest, 'name')
	net = getJSONValue(manifest, 'net')
	print(mission + net)
	if mission == "Key not found" or net == "Key not found":
		print(f":(")
		print(f"Your computer didn't run into a problem and doesn't need to restart. We didn't collect anything and we won't restart for you. ")
		print(f"Stop code: ")
		return ":("
	print(f"Next launch: {mission} at {net}")		

main() # FINALLY!!!!!1