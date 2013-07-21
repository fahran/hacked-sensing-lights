import requests
import json
import time

class light():
    hueCap = 65535
    blue = 43000
    purple = 60000
    red = 65535

    def __init__(self, id, cycleFlag = False, pulseFlag = False, pulseOnceFlag = False, tempFlag = False):
        self.getUrl = "http://192.168.2.76/api/fahranHacked/lights/" + str(id)
        self.updateUrl = self.getUrl + "/state"

        self.id = id
        self.cycleFlag = cycleFlag
        self.pulseFlag = pulseFlag
        self.pulseOnceFlag = pulseOnceFlag
        self.tempFlag = tempFlag
        self.pulseState = 0
        self.pulse = False
        self.maxBri= 200
        self.minBri = 10
        self.briShift = 100
        self.bri = json.loads(requests.get(self.getUrl).text)["state"]["bri"]
        self.colour = json.loads(requests.get(self.getUrl).text)["state"]["hue"]
        self.sat = json.loads(requests.get(self.getUrl).text)["state"]["sat"]
        self.lastUpdateTime = time.time()
        self.tempValue= 0

        self.transitionTime = 5
        self.setTransitionTime(self.transitionTime)
        self.enable(True)
        self.state = "calm"
        self.lastState = "calm"

    def setHue(self, hue):
        payload = {'hue': hue}
        requests.put(self.updateUrl, data=json.dumps(payload))

    def enable(self, state):
        requests.put(self.updateUrl, data=json.dumps({"on":state}))

    def shiftColour(self, val):
        self.colour = (self.colour + val) % self.hueCap
        requests.put(self.updateUrl, data=json.dumps({"hue":self.colour}))

    def setTransitionTime(self, val):
        requests.put(self.updateUrl, data=json.dumps({"transitiontime":val}))

    def shiftBrightness(self, val):
        self.bri = (self.bri + val)
        self.bri = max(self.minBri, self.bri)
        self.bri = min(self.maxBri, self.bri)

        requests.put(self.updateUrl, data=json.dumps({"bri":self.bri}))

    def updateColour(self):
        if self.cycleFlag:
            self.shiftColour(1000)

    def setColour(self, value):
        print value
        requests.put(self.updateUrl, data=json.dumps({"hue":value}))

    def updateBrightness(self):
        if self.pulseFlag:
            if self.pulse:
                if self.bri < self.maxBri:
                    self.shiftBrightness(self.briShift)

            else:
                if self.bri > self.minBri:
                    self.shiftBrightness(-self.briShift)

    def pulseOnce(self):
        if self.pulseOnceFlag:
            if self.pulseState == 0:
                self.shiftBrightness(self.briShift)
                if self.bri == self.maxBri:
                    self.pulseState = 1
            else:
                if self.pulseState == 1:
                    self.shiftBrightness(-self.briShift)
                    if self.bri == self.minBri:
                        self.pulseState = 0
                        self.pulseOnceFlag = False

    def tempToColour(self):
        if self.tempFlag:
            value = self.tempValue
            lastState = state
            if value <= 5:
                #chilled
                self.setColour(self.blue)
                self.state = "calm"

            else:
                if  value >= 18:
                    #panic mode - you're melting!
                    self.setColour(self.red)
                    self.shiftBrightness(255)
                    self.pulseFlag = True
                    self.state = "fire"
                else:
                    if value > 10:
                        value = 10
                    colour = self.blue + ((self.purple-self.blue) * (value/10))
                    print colour
                    self.setColour(colour)
                    self.state = "active"

    def update(self):
        if time.time() - self.lastUpdateTime > self.transitionTime*.01: #transitionTime in 100ths of a second
            self.lastUpdateTime = time.time()
            self.updateColour()
            self.updateBrightness()
            self.pulseOnce()
            self.tempToColour()

def main():
    lamp = light(1)
    lamp.cycleFlag = False
    lamp.pulseFlag = False
    lamp.setHue(0)
    lamp.pulse = True
    pulsePhase = 3

    pulseTime = time.time()

    while True:
        lamp.update()
        if time.time() - pulseTime > pulsePhase:
            lamp.pulseOnceFlag = True
            pulseTime = time.time()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        quit
    except KeyboardInterrupt:
        quit

