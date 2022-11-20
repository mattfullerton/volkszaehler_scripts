# Read the output of the mbus-test program ("main")
import requests

value = None

with open("output.txt", "r") as ofile:
    while True:
        line = ofile.readline()
        if line == "":
            print("Found no entry")
            break
        #print(line)
        if "Energy (kWh)" in line:
            ofile.readline()
            valueLine = ofile.readline()
            value = int((valueLine.split("result: ")[1].split("\t")[0]))
            if value > 0:
                print("Read " + str(value) + " kWh")
                break

if value is not None:
    print("Sending to Volkszähler")
    pushUrl = "http://192.168.0.215/middleware/data/77bde810-65ef-11ed-a456-d344cac2e6de.json?operation=add&value=" + str(value)
    print("Sending request: " + pushUrl)
    pushResult = requests.get(pushUrl)
