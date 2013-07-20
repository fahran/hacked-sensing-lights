import serial
#python -m serial.tools.list_ports <-will print list of available ports
#port = serial.Serial(0) #open first port, no time out
port = serial.Serial(0, 9600, timeout = 5) #first port, baudrate = 9600, timeout = 5s
print port.portstr #print what port was used

#line = port.readline()
#print output + str(line)
for line in port:
	print line