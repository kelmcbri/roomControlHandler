#!/usr/bin/env python
# This program is used by RoomControlHandler.py to control an external Video Switch.
#
from threading import Thread
import Config
import serial
import time

class ESDSControl(Thread):
        def __init__(self,message="0",port="/dev/cu.usbserial",baud=9600):
          self.port = port
          self.baud = baud
          self.message = message
          
          Thread.__init__(self)
          self.port = port
          self.baud = baud
          self.message = message
        
        def run(self):
                print("Trying serial port with message "+str(self.message))
                try:
                        ser = serial.Serial(self.port, self.baud, write_timeout=3)
#                ser = serial.Serial(port="/dev/cu.usbserial",baud=9600,timeout=1)
#                ser = serial.Serial(port="/dev/cu.usbserial")
                # open the serial port
                        if ser.isOpen():
                                print(ser.name + ' is open...')
                                if self.message == 1:
                                     cmd = 'port0R'
                                     cmd_as_bytes = str.encode(cmd)
                                elif self.message == 2:
                                     cmd = 'port1R'
                                     cmd_as_bytes = str.encode(cmd)
                                elif self.message == 3:
                                     cmd = 'port2R'
                                time.sleep(1)     
                                ser.write(cmd_as_bytes)
                                print("We sent "+ cmd)
                        else:
                         print("message did not match any port number " + self.message)
                        time.sleep(1) 
                        ser.close()
                        print("Serial Port is closed")
                except:
                 print("Was not able to open Serial Port")
                if ser.isOpen():
                        ser.close()

if __name__ == '__main__':
        ESDSControl()