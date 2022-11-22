# Read the output of the mbus-test program ("main")
import requests

meter_channel = "77bde810-65ef-11ed-a456-d344cac2e6de"
power_channel = "efc98650-6a33-11ed-b409-318a2275d4f2"

mvalue = None
pvalue = None

with open("output.txt", "r") as ofile:
    while True:
        line = ofile.readline()
        # Detect EOF
        if line == "":
            print("Found no entry")
            break
        if "Energy (kWh)" in line:
            ofile.readline()
            valueLine = ofile.readline()
            mvalue = int((valueLine.split("result: ")[1].split("\t")[0]))
            if mvalue > 0:
                print("Read " + str(mvalue) + " kWh")
        if "Power (W)" in line:
            ofile.readline()
            valueLine = ofile.readline()
            pvalue = int((valueLine.split("result: ")[1].split("\t")[0]))
            if pvalue > 0:
                print("Read " + str(pvalue) + " W")
                break

if mvalue is not None:
    print("Sending to Volkszähler")
    pushUrl = "http://192.168.0.215/middleware/data/" + meter_channel + ".json?operation=add&value=" + str(mvalue)
    print("Sending request: " + pushUrl)
    pushResult = requests.get(pushUrl)
if pvalue is not None:
    pushUrl = "http://192.168.0.215/middleware/data/" + power_channel + ".json?operation=add&value=" + str(pvalue)
    print("Sending request: " + pushUrl)
    pushResult = requests.get(pushUrl)
