#!/usr/bin/env bash
cd /root/scripts/volkszaehler_scripts/readHeat
rm startup.txt
rm output.txt
# Wait a little, so that all system startup etc. is complete and we can run at a normal speed
sleep 60
# Tell program to send wake up command
# TODO: I think it might do this before every other command too, so unnecessary?
echo "1" | ./main > startup.txt &
# Give time to complete
sleep 3
# We're done with our first run
pkill -9 main &
# Time for process killing
sleep .5
# Tell program to send data request command
echo "3" | ./main > output.txt &
# Give time to complete
sleep 40
# Done with data reading
pkill -9 main &
# Wait a bit longer
sleep 20
# For debugging purposes, output what we got
cat output.txt
# Interpret the output
python3 readHeat.py
# Tell system to go to sleep in 5 minutes
/usr/sbin/shutdown +5
