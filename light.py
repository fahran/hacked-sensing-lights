import requests
import json
import time

class light():
    hueCap = 65280

    def __init__(self, id, cycleFlag, pulseFlag):
        self.getUrl = "http://192.168.2.76/api/fahranHacked/lights/" + str(id)
        self.updateUrl = self.getUrl + "/state"

        self.id = id
        self.cycleFlag = False
        self.pulseFlag = False
        self.pulse = False
        self.maxBri= 255
        self.minBri = 10
        self.briShift = 2.0
        self.bri = json.loads(requests.get(self.getUrl).text)["state"]["bri"]
        self.colour = json.loads(requests.get(self.getUrl).text)["state"]["hue"]
        self.lastUpdateTime = time.time()

        self.setTransitionTime(2)

    def setHue(self, hue):
        payload = {'hue': hue}
        requests.put(self.updateUrl, data=json.dumps(payload))

    def enable(self):
        requests.put(self.updateUrl, data=json.dumps({"on":"true"}))

    def shiftColour(self, val):
        self.colour = (self.colour + val) % self.hueCap
        requests.put(self.updateUrl, data=json.dumps({"hue":self.colour}))

    def setTransitionTime(self, val):
        requests.put(self.updateUrl, data=json.dumps({"transitiontime":val}))

    def shiftBrightness(self, val):
        self.bri = (self.bri * val)
        self.bri = max(self.minBri, self.bri)
        self.bri = min(self.maxBri, self.bri)

        requests.put(self.updateUrl, data=json.dumps({"bri":self.bri}))

    def updateColour(self):
        if self.cycleFlag:
            self.shiftColour(1000)

    def updateBrightness(self):
        if self.pulseFlag:
            if self.pulse:
                if self.bri < self.maxBri:
                    self.shiftBrightness(self.briShift)

            else:
                if self.bri > self.minBri:
                    self.shiftBrightness(1/self.briShift)

    def update(self):
        if time.time() - self.lastUpdateTime > 0.2:
            self.lastUpdateTime = time.time()
            self.updateColour()
            self.updateBrightness()


if __name__ == '__main__':
    light = light(1)
    light.cycleFlag = False
    light.pulseFlag = True
    light.setHue(0)
    light.pulse = True

    pulseTime = time.time()

    while True:
        currentTime = time.time()
        if currentTime - pulseTime > 1:
            pulseTime = currentTime
            light.pulse = not light.pulse
        light.update()
