#!/usr/bin/env bash
cd /root/scripts/mbus
rm startup.txt
rm output.txt
echo "1" | ./main > startup.txt &
sleep 3
pkill -9 main &
sleep .5
echo "3" | ./main > output.txt &
sleep 40
pkill -9 main &
sleep 20
cat output.txt
python3 readHeat.py
/usr/sbin/shutdown +5
