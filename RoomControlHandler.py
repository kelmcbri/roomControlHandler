#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Initial Code from https://github.com/gbraux/Cisco-Showroom-RoomControl by Guillaume BRAUX
# This tweak of the original code created by Keller McBride 07/20/2017   kelmcbri@cisco.com
#
# Purpose:
#	If more Video input sources are needed on a Cisco Video Codec, this program allows an
#	external video switcher to be coupled to a port on the Cisco Video Codec.  The external
#	video switcher is controlled by the Cisco Touch 10 tablet interface.
#
# Files:
#	RoomControlHandler.py 		- Main Program.
#						Launches Threaded Web Server
#						Sets up new Video Sources on Cisco Video Codec
#						Registers for Feedback on Inputs from Cisco Video Codec
#							Re-registers for feedback periodically
#	Config.py	  		- Configuration Paramters
#	CondecControl.py		- Send and Receive commands for Video Codec
#	ExternalHDMISwitchControl.py	- Send commands for HDMI Video Switcher
#		class ESDSControl	- Serial Controller for E-SDS brand 3 port HDMI video switcher
#
# Components:
#	E-SDS UHD 4K@60Hz HDMI Switch,3x1 HDMI Powered Switch with IR Wireless Remote, HDMI 2.0, HDCP 2.2, and RS232
#		https://www.amazon.com/gp/product/B01G53WV20/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1
# 	Cisco SX series Video Codec
#	Controller - i.e. Server Running this python3 program - Macbook or Raspbery Pi or Cisco IR829, etc. 
#
import http.server
import http.client
import socketserver
import base64
import re				# Used for Pattern Matching regular expressions
#import sqlite3
import datetime
import urllib.parse
import json
import threading
import time
import sys
import signal
import logging
import cgi
import urllib.request
#import xml.etree.ElementTree as ET

# Librairies
import Config   			# Use this file to set IP Addresses of components and other parameters
import CodecControl 			# CodecControl sends/receives data via http to Cisco Codecs running CE code
import ExternalHDMISwitchControl	# Create a class in this file for each type of external video switch you want to control

#inputValue = 0
#outputValue = 1
#presetValue = 4
#inputNames = ["AppleTV","Spycam","CableTV"]
#outputNames = ["","TVDroite","TVCentre","TVGauche","MX300","MX800","Inexistant","Inexistant","Spycam"]

controllerIP = Config.controller['ip']
controllerPort = Config.controller['port']

global debug
debug = Config.debugMode

def startThread():
	
	if Config.debugMode == 'True' :
		print("--- Trying to Start Web Server  ("+controllerIP+":"+str(controllerPort)+") ---")
	server = ThreadedHTTPServer(('0.0.0.0', controllerPort), MyRequestHandler)
	print('Starting server, use <Ctrl-C> to stop')
	
	thread = threading.Thread(target = server.serve_forever)
	thread.deamon = False
	thread.start()
	
	if Config.debugMode == 'True' :
		print("---  New Web Service started at ("+controllerIP+":"+str(controllerPort)+") ---")
	return server

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
	
	def do_POST(self):
	
		print("POST RECEIVED")
		
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()
		content_len = int(self.headers.get("Content-Length"))
		post_body = self.rfile.read(content_len).decode("utf-8")
		if Config.debugMode == 'True' :
			print(post_body)
		
		CodecEventHandler(post_body)
		
	def log_message(self, format, *args):
		sys.stdout.write("%s --> [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

def CodecEventHandler(xmlData):

	global outputValue	
	global inputValue
	global presetValue
	global proxixi
	global codecs

	print("---- Handling Codec Event ----")
	print("XML RECU")
	if Config.debugMode == 'True' :
		print(xmlData)
		
	if ((Config.codecs["grandOleOpry"]["mac"] in xmlData) and ("AppleTV"  in xmlData)):
		print("Apple TV Selected")
		myThreadObject = ExternalHDMISwitchControl.ESDSControl(message=1)
		myThreadObject.start()
		myThreadObject.join()

	if ((Config.codecs["grandOleOpry"]["mac"] in xmlData) and ("CableTV"  in xmlData)):
		print("Cable TV Selected")
		myThreadObject = ExternalHDMISwitchControl.ESDSControl(message=2)
		myThreadObject.start()
		myThreadObject.join()

	if ((Config.codecs["grandOleOpry"]["mac"] in xmlData)  and ("SpyCam"  in xmlData)):
		print("SpyCam Selected")		
		myThreadObject = ExternalHDMISwitchControl.ESDSControl(message=3)
		myThreadObject.start()
		myThreadObject.join()

def RemoveCodecsPresentationSource():
	presentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<RemoveAll command=\"True\">"
						"</RemoveAll>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")

	if Config.debugMode == 'True' :
		print("Sending new input source info to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], presentationSourcegrandOleOpry)

def SendCodecsPresentationSource():
	presentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<Add command=\"True\">"
							"<ConnectorId>3</ConnectorId>"
							"<Name>AppleTV</Name>"
							"<SourceIdentifier>AppleTV</SourceIdentifier>"
							"<Type>mediaplayer</Type>"
						"</Add>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")

	if Config.debugMode == 'True' :
		print("Sending new input source info to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], presentationSourcegrandOleOpry)
	
	presentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<Add command=\"True\">"
							"<ConnectorId>3</ConnectorId>"
							"<Name>SpyCam</Name>"
							"<SourceIdentifier>SpyCam</SourceIdentifier>"
							"<Type>camera</Type>"
						"</Add>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")

	if Config.debugMode == 'True' :
		print("Sending new input source info to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], presentationSourcegrandOleOpry)
	
	presentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<Add command=\"True\">"
							"<ConnectorId>3</ConnectorId>"
							"<Name>CableTV</Name>"
							"<SourceIdentifier>CableTV</SourceIdentifier>"
							"<Type>desktop</Type>"
						"</Add>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")

	if Config.debugMode == 'True' :
		print("Sending new input source info to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], presentationSourcegrandOleOpry)	

def SetCodecPresentationSourceStatus():
	enablePresentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<State>"
							"<Set command=\"True\">"
								"<State>Ready</State>"
								"<SourceIdentifier>AppleTV</SourceIdentifier>"			
							"</Set>"	
						"</State>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")
	if Config.debugMode == 'True' :
		print("Setting new input source Status ENABLE to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], enablePresentationSourcegrandOleOpry)	

	enablePresentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<State>"
							"<Set command=\"True\">"
								"<State>Ready</State>"
								"<SourceIdentifier>SpyCam</SourceIdentifier>"			
							"</Set>"	
						"</State>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")
	if Config.debugMode == 'True' :
		print("Setting new input source Status ENABLE to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], enablePresentationSourcegrandOleOpry)

	enablePresentationSourcegrandOleOpry = (
		"<Command>"
			"<UserInterface>"
				"<Presentation>"
					"<ExternalSource>"
						"<State>"
							"<Set command=\"True\">"
								"<State>Ready</State>"
								"<SourceIdentifier>CableTV</SourceIdentifier>"			
							"</Set>"	
						"</State>"
					"</ExternalSource>"
				"</Presentation>"
			"</UserInterface>"
		"</Command>")
	if Config.debugMode == 'True' :
		print("Setting new input source Status ENABLE to codec \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], enablePresentationSourcegrandOleOpry)

def SendCodecsFeedbackReg():
	feedbackReggrandOleOpry = (
		"<Command>"
			"<HttpFeedback>"
				"<Register command=\"True\">"
					"<FeedbackSlot>2</FeedbackSlot>"
					"<ServerUrl>http://"+controllerIP+":"+str(controllerPort)+"</ServerUrl>"
					"<Expression item=\"1\">/Event/UserInterface/Presentation/ExternalSource</Expression>"
				"</Register>"
			"</HttpFeedback>"
		"</Command>")
		
	if Config.debugMode == 'True' :
		print("Requesting Codec HTTPFeedback Registration \r\n")
	CodecControl.SendXMLDataToCodec(Config.codecs["grandOleOpry"], feedbackReggrandOleOpry)
	print("Feedback Codec HTTPFeedback Completed")

def signal_term_handler(signal, frame):
	print('got SIGTERM')
	sys.exit(0)
		
try:
	if __name__ == "__main__":
		
		signal.signal(signal.SIGTERM, signal_term_handler)
		
		print ("The current debugMode set in Config.py is "+Config.debugMode)
		time.sleep(2)
		server = startThread()
		
		ct = time.time()
		# Remove Existing External Presentation Sources
		RemoveCodecsPresentationSource()
		time.sleep(3)
		# Setup external hdmi input sources
		SendCodecsPresentationSource()
		# Enable external hdmi input sources			
		SetCodecPresentationSourceStatus()

		
		while True:
			# Regularly manage the recording of HTTP feedback
			SendCodecsFeedbackReg()	
			time.sleep(60)

except (KeyboardInterrupt, SystemExit):
	server.shutdown()
	print("--- WEB Server stopped ---")

	sys.exit(0)