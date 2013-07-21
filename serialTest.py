import serial, copy
from serial.tools import list_ports
from copy import *
#python -m serial.tools.list_ports <-will print list of available ports
#port = serial.Serial(0) #open first port, no time out
#port = serial.Serial(2, 9600, timeout = 5) #third port (i have three ports on my laptop, this happens to be the one I had that was free, baudrate = 9600, timeout = 5s
port = None

class tracker():
    def __init__(self, steps):
        self.firstUpdate = True
        self.lastVal = 0.0
        self.difference = 0.0
        self.val = 0.0
        self.steps = steps
        self.avStep = 0
        self.runningTotal = 0.0

    def averageUpdate(self, value):
        #add result to total.  If step has progressed far enough, return average
        self.avStep += 1
        self.runningTotal += value
        if self.avStep == self.steps:
            average = self.runningTotal/self.avStep
            self.runningTotal = 0.0
            self.avStep = 0
            return average
        else:
            return -1

class changeTracker(tracker):
    def update(self, value):
        self.val = value
        if self.firstUpdate:
            self.lastVal = copy(self.val)
            self.firstUpdate = False
        self.difference = self.val - self.lastVal
        self.lastVal = copy(self.val)
        #check for returned result
        result = self.averageUpdate(self.difference)
        return result #returns -1 until given values processed

class valueTracker(tracker):
    def update(self, value):
        result = self.averageUpdate(value)
        return result #returns -1 until given values processed


def init():
    #global port
    portsList = list_ports.comports()
    print portsList
    for item in portsList:
        #print item
        portName = item[0]
        #print portName
        portNumber = int(portName[3]) - 1
        #print portNumber
        try:
            port = serial.Serial(portNumber, 9600, timeout = 5)
            print "Using serial connection on " + str(port.portstr) #print what port was selected... hopefully should work fine if there's only 1!
        except:
            print "No port active!"
        return port

def main():
        heatChange = changeTracker(5) #averages change over (x) readings
        heatValue = valueTracker(5)
        #continuous loop taking value from serial port
        for line in port:
                #print line
                values = str.split(line)
                temp = float(values[0])
                #sensor = values[1]
                print temp
                #print sensor

                #tracker updates
                tempChange = heatChange.update(temp)
                #periodically returns average value:
                if not tempChange == -1:
                    #action on valid response:
                    print "Temperature change: " + str(tempChange)

                tempValue = heatValue.update(temp)
                if not tempValue == -1:
                    #action on valid response:
                    print "Current temperature: " + str(tempValue)




if __name__ == '__main__':
    try:
        port = init()
        main()
    except SystemExit:
        quit
    except KeyboardInterrupt:
        quit