#!/usr/bin/env python3

############# TERMINAL SPACEFLIGHT #############
### Gets latest launch and prints it to bash ###
############# Made by Sam Rohrbach #############

import sys
import signal
import requests
import json
import os
import platform
import argparse
from datetime import *

runningOn = platform.system()
fileName = ".terminalSpaceflightTempFile.json"
badVal = "{'name':'no','net':'whenever'}" # something is better than nothing
tmpFileLinux = "~/" # or whatever
tmpFileWindows = "%TEMP%\\"
tmpFileMac = "$tmpFile/"
url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&mode=list&offset=1" # launchlibrary2 2.3, only the next launch in list

if runningOn == "Linux":
	tmpFile = tmpFileLinux + fileName
elif runningOn == "Windows":
	tmpFile = tmpFileWindows + fileName
elif runningOn == "Darwin":
	tmpFile = tmpFileMac + fileName

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

def parseArgs(): # do some cmd line parse things or whatever
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", help = "Display extra messages so you know what's going on", action = "count", default=0)
	parser.add_argument("-?", "--help", help = "Displays next rocket launch date and time in terminal from LaunchLbrary2 API", default=0)
	return parser.parse_args()

def main():
	manifest = "" # make sure it exists first
	# does file exist?
	try:
		if os.path.exists(tmpFile):
			#print(f"Cache already exists at {tmpFile}")
			lastModifiedDate = whenLastModified(tmpFile)
			timeDifference = datetime.now() - lastModifiedDate
			if (timeDifference < timedelta(minutes=10)):
				#print(f"Cache was modified recently at {lastModifiedDate}, skipping overwrite")
				whatever = "blah blah placeholder" # prevent errors from there being nothing in here
			elif manifest == badVal or manifest == "":
				saveJSON(fetchJSON(url), tmpFile)
				#print(f"Cache is bad, JSON data saved to {tmpFile}")
				#print(f"Last modified: {whenLastModified(tmpFile)}")		
			else:
				jsonData = fetchJSON(url)
				saveJSON(jsonData, tmpFile)
				#print(f"JSON data saved to {tmpFile}")
				#print(f"Last modified: {whenLastModified(tmpFile)}")
		else:
			fileThing = open(tmpFile, "w")
			fileThing.write(badVal)
			#print(f"Cache does not exist at {tmpFile}, creating one")
			with open(tmpFile, "r") as fileThing:
				manifest = fileThing.read()
			jsonData = fetchJSON(url)
			saveJSON(jsonData, tmpFile)
			#print(f"JSON data saved to {tmpFile}")
			#print(f"Last modified: {whenLastModified(tmpFile)}")
	except FileNotFoundError:
		fileThing = open(tmpFile, "w")
		fileThing.write(badVal)
		#print(f"Cache does not exist at {tmpFile}, creating one")
		with open(tmpFile, "r") as fileThing:
			manifest = fileThing.read()
		jsonData = fetchJSON(url)
		saveJSON(jsonData, tmpFile)
		#print(f"JSON data saved to {tmpFile}")
	
	with open(tmpFile, "r") as fileThing:
		manifest = fileThing.read()
	
	#print(manifest) # uncomment for debugging

	# get actual data
	wholeThing = json.loads(manifest)
	mission = wholeThing["results"][0]["name"]
	mission = str(mission)
	net = wholeThing["results"][0]["net"]
	net = str(net)
	net.replace("Z", "")
	netFormatted = datetime.fromisoformat(net)
	netFormatted = str(netFormatted)
	netFormatted.replace("+00:00", "")
	return(f"Next launch: {mission} | {netFormatted}")
	#return results

print(f"{main()}") # hey look you found me
