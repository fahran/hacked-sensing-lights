import json
import requests
import time

baseurl = "http://192.168.2.76/api/fahranHacked"
light1 = "/lights/1/state"

hueCap = 65280

def enableLight(val):
    url = baseurl + "/lights/" + str(val) + "/state"
    requests.put(url, data=json.dumps({"on":"true"}))

def incrementColour(light, val):
    getUrl = baseurl + "/lights/" + str(light) + "/"
    putUrl = baseurl + "/lights/" + str(light) + "/state"
    response = requests.get(getUrl).text
    responseDict = json.loads(response)
    currentCol = responseDict["state"]["hue"]
    print currentCol
    col = currentCol + val
    if col > hueCap:
        col -= hueCap
    requests.put(putUrl, data=json.dumps({"hue":col}))

def main():
    enableLight(1)
    while True:
        incrementColour(1, 1000)
        time.sleep(0.4)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        quit
    except KeyboardInterrupt:
        quit