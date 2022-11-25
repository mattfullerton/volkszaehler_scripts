# License: MIT
# Author: Matt Fullerton

# Quick interactive script for entering water meter values into Volkszähler
# It tries to automate as much as possible

import requests
import time
import datetime


# IP or host of your Volkszähler
instance = "volkszaehler"
# http or https
protocol = "http"
# In days - how far back to look for the last reading
look_back_time = 2

water_counters = []

print("Gathering your current water values, this might take a moment...")
all_channels = requests.get(protocol + "://" + instance + "/middleware/channel.json").json()

for channel in all_channels["channels"]:
    if channel["type"] ==  "watertotal":
        water_counters.append([channel["title"], channel["uuid"]])

# Put the channels in some order so it will hopefully make data entry easier
water_counters.sort(key=lambda x: x[0])

for channel in water_counters:
    # Search window for last result; VZ wants TSs in ms
    current_ts = round(time.time())
    from_ts = (current_ts - (look_back_time * 24 * 60 * 60)) * 1000
    current_ts *= 1000
    getUrl = protocol + "://" + instance + "/data/" + channel[1] + ".json?from=" + str(from_ts) + "&to=" + str(current_ts) + "&options=raw"
    chanData = requests.get(getUrl).json()
    last_meas = ""
    try:
        last_meas = chanData["data"]["tuples"][-1][1]
        channel.append(last_meas)
        print(channel[0] + " - last reading: " + str(last_meas) + " litres")
    except IndexError:
        channel.append("")
        print(channel[0] + " last reading unknown.")

print("\nPlease enter the current readings (if you want to skip a reading, enter 'X'):")

water_counters_send = []

for channel in water_counters:
    new_val = input(channel[0] + " - [" + str(channel[2]) + "]: ")
    try:
        # Use the cast to int to check if its a valid integer
        channel.append(int(new_val))
        if channel[2] != "" and channel[3] < channel[2]:
            print("Bad input detected for " + channel[0] + " - will skip")
        else:
            water_counters_send.append(channel)
    except ValueError:
        # Skip if they entered x
        if new_val.lower() != 'x':
            # If we have a last measurement...
            if channel[2] != "":
                # Take last value as a genuine measurement that nothing changed - 0l/h
                channel.append(channel[2])
                water_counters_send.append(channel)

print("\nGoing to send the following updates - hit enter to continue (Ctrl-C to abort):")
for channel in water_counters_send:
    print(channel[0] + " - new reading: " + str(channel[3]) + " litres")
input("")

for channel in water_counters_send:
    pushUrl = protocol + "://" + instance + "/middleware/data/" + channel[1] + ".json?operation=add&value=" + str(channel[3])
    if channel[0] == "Washing Machine":
        tsd = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 10, 0, 0)
        tsts = int(time.mktime(tsd.timetuple()))
        pushUrl += "&ts=" + str(tsts * 1000)
        print("Note: Washing Machine will be set to 10am today - are you sure?")
        input("")
    print("Sending request: " + pushUrl)
    pushResult = requests.get(pushUrl)
