import serial, copy
from serial.tools import list_ports
from copy import *
#python -m serial.tools.list_ports <-will print list of available ports
#port = serial.Serial(0) #open first port, no time out
#port = serial.Serial(2, 9600, timeout = 5) #third port (i have three ports on my laptop, this happens to be the one I had that was free, baudrate = 9600, timeout = 5s
port = None
class changeTracker():
        def __init__(self):
                self.firstUpdate = True
                self.lastVal = 0.0
                self.difference = 0.0
                self.val = 0.0
                
        def update(self, value):
                self.val = value
                if self.firstUpdate:
                        self.lastVal = copy(self.val)
                        self.firstUpdate = False
                        print "first update"
                print "current " + str(self.val)
                print "last " + str(self.lastVal)
                self.difference = self.val - self.lastVal
                print "change: " + str(self.difference)
                self.lastVal = copy(self.val)

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
                        print port.portstr #print what port was selected... hopefully should work fine if there's only 1!

                except:
                        print "No port active!"
                return port
        

def main():
        changeTrace = changeTracker()
        #continuous loop taking value from serial port
        for line in port:
                #print line
                values = str.split(line)
                temp = float(values[0])
                sensor = values[1]
                print temp
                print sensor
                changeTrace.update(temp)
                

if __name__ == '__main__':
    try:
        port = init()
        main()
    except SystemExit:
        quit()
                
