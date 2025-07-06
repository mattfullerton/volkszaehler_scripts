import requests

data = requests.get("---hoymiles-reader---/api/livedata/status").json()

print(data)

if data["inverters"][0]["producing"]:
    kwh = data["total"]["YieldTotal"]["v"]
    requests.get("http://---raspberrypi---/middleware/data/3d511ee0-6814-11ed-876c-b9901539cbc3.json?operation=add&value=" + str(kwh))
