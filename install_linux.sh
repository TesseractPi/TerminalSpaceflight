#!/bin/bash

echo This script will use pyinstaller to make an executable. It will then make a symlink to /usr/bin and be available globally This will require sudo.
echo
echo If you don\'t want to install this, press Ctrl-C. 
sleep 1
echo 5...
sleep 1
echo 4...
sleep 1
echo 3...
sleep 1
echo 2...
sleep 1
echo 1...
sleep 1
echo Commencing install...
pyinstaller --onefile nextlaunch.py
sudo ln -vsf $(which dist/nextlaunch) /usr/bin/nextlaunch
echo Install complete! Run this again when reinstalling or updating Terminal Spaceflight. 
