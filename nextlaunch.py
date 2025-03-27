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
fileName = ".nextlaunch.json"
badVal = "{'name':'Error | Manifest file is bad. To fix, wait 15 minutes or delete ~/.nextlaunch.json','net':'1970-01-01'}" # something is better than nothing
url = "https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=1&mode=list&offset=1" # launchlibrary2 2.3, only the next launch in list

# because C:\ is just a windows thing
if runningOn == "Linux" or "Darwin":
	tmpFile = os.path.expanduser("~/") + fileName
elif runningOn == "Windows":
	tmpFile = os.environ.get('TEMP', '') + "\\" + fileName

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

def parseArgs(): # do some cmd line parse things or whatever, added by github copilot 
	parser = argparse.ArgumentParser("Terminal Spaceflight")
	parser.add_argument("-v", "--verbose", help = "Display verbose information for debugging", action = "count", default=0)
	return parser.parse_args()

def main():
	args = parseArgs()
	manifest = "" # make sure manifest exists first
	# does temp file exist?
	try:
		if os.path.exists(tmpFile):
			if args.verbose:
				print(f"Cache already exists at {tmpFile}")
			lastModifiedDate = whenLastModified(tmpFile)
			timeDifference = datetime.now() - lastModifiedDate
			if (timeDifference < timedelta(minutes=10)):
				if args.verbose:
					print(f"Cache was modified recently at {lastModifiedDate}, skipping overwrite")
			elif manifest == badVal or manifest == "":
				saveJSON(fetchJSON(url), tmpFile)
				if args.verbose:
					print(f"Cache is bad, JSON data saved to {tmpFile}")
					print(f"Last modified: {whenLastModified(tmpFile)}")		
			else:
				jsonData = fetchJSON(url)
				saveJSON(jsonData, tmpFile)
				if args.verbose:
					print(f"JSON data saved to {tmpFile}")
					print(f"Last modified: {whenLastModified(tmpFile)}")
		else:
			fileThing = open(tmpFile, "w")
			fileThing.write(badVal)
			if args.verbose:
				print(f"Cache does not exist at {tmpFile}, creating one")
			with open(tmpFile, "r") as fileThing:
				manifest = fileThing.read()
			jsonData = fetchJSON(url)
			saveJSON(jsonData, tmpFile)
			if args.verbose:
				print(f"JSON data saved to {tmpFile}")
				print(f"Last modified: {whenLastModified(tmpFile)}")
	except FileNotFoundError:
		fileThing = open(tmpFile, "w")
		fileThing.write(badVal)
		if args.verbose:
			print(f"Cache does not exist at {tmpFile}, creating one")
		with open(tmpFile, "r") as fileThing:
			manifest = fileThing.read()
		jsonData = fetchJSON(url)
		saveJSON(jsonData, tmpFile)
		if args.verbose:
			print(f"JSON data saved to {tmpFile}")
	
	with open(tmpFile, "r") as fileThing:
		manifest = fileThing.read()
	
	if args.verbose:
		print("Launch manifest is as follows: ")
		print(" ")
		print(manifest) # uncomment for debugging

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

print(f"{main()}") # oh no there's an error :(
