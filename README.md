# Terminal Spaceflight
### A python script to display next rocket launch in terminal
#### By Sam Rohrbach

****

Terminal Spaceflight is a small project I made to merge two interests of mine  - the terminal and spaceflight. It uses the [LaunchLibrary2 API](https://ll.thespacedevs.com/docs/) to fetch the next rocket launch. 

Since the free tier of the LL2 API is rate-limited to 15 calls per hour, this program stores a temporary cache file in `/tmp/nextlaunch.json` for Linux, `$TMPDIR/nextlaunch.json`, or `%tmpdir%\nextlaunch.json` for Windows. It then reads from this file and displays its data in Bash. However, if the file has been modfied more than 10 minutes ago, it will fetch new data from LL2. 

This is an ongoing project, so expect some updates to this project over time. 
