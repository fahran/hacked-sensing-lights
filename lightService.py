import requests
import json

baseUrl = "http://192.168.2.76/api/fahranHacked/"

def turnMiddleLightToHue(hue):
	turnLightToHue(1, hue)

def turnLightToHue(lightId, hue):
    payload = {'hue': hue}
	url = baseUrl + "lights/" + lightId + "/state"
	requests.put(url, data=json.dumps(payload))