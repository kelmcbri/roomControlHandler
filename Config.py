#!/usr/bin/env python
# This config file is used to hold site specific information used by RoomControlHandler.py
# *** Please edit the following values based on your environement
#
debugMode = "True" # If set to TRUE then print out a bunch of debug information to terminal when running program.

# IP Address for the server running this program.  This IP and port will be used to register httpfeedback from the codec.
# "controller" is whatever device is running RoomControlHandler.py. ie Macbook, Raspberry Pi, Cisco IR829, etc.
controller = {"ip": "10.150.182.100", "port": 1214}

# "codecs" are the Cisco SX video codecs being managed by RoomControlHandler.py. The first datapoint in codecs is the name
# of the codec which would likely be the name of the conference room the codec is in
codecs = {"grandOleOpry": {"ip": "10.150.183.17", "user": "kelmcbri", "password":"C1sc0123","mac":"e4:c7:22:6a:40:04","connectorID":"3","input1Name":"AppleTV","input2Name":"SpyCam","input3Name":"CableTV" },
          "vangogh": {"ip": "10.1.110.31", "user": "kelmcbri", "password":"C1sc0123","mac":"E4:C7:22:66:61:6C" }}

endpointGenericAuthRealm = "Basic YWRtaW46";