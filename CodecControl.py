#!/usr/bin/env python
# This program is used by RoomControlHandler.py to send and recieve commands with Cisco SX Video Codec
#
import ssl
import http.client
import base64
import Config

def SendXMLDataToCodec(codec,xml_data):
	if Config.debugMode == 'True' : print("Begin sending data to codec")
	
	if ((codec["user"] != None) & (codec["password"] != None)):
		authRealm = base64.b64encode(str.encode(codec["user"]+":"+codec["password"])).decode("ascii");
		if Config.debugMode == 'True' : print("Username/Pass SET")
	else:
		authRealm = Config.endpointGenericAuthRealm
		if Config.debugMode == 'True' : print("Using Default Passwords")

	ctx=ssl._create_unverified_context()	

	conn = http.client.HTTPSConnection(codec["ip"], context=ctx)
	if Config.debugMode == 'True' : print("Request :")
	payload = xml_data.encode('utf-8')
	if Config.debugMode == 'True' :  print(payload)

	headers = {
		'authorization': "Basic "+authRealm,
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache",
		'postman-token': "b5f016ed-5e19-d311-563e-c6aa7fdaa591"
		}

	try:
		conn.request("POST", "/putxml", payload, headers)
		res = conn.getresponse()
		data = res.read()
	except:
		e = conn.HTTPException
		print (e)
		print("EXCEPTION!!!   --- Error sending data to codec")
		return
		

	if Config.debugMode:
		print("\r\nResponse:")
		print(data.decode("utf-8"))
	print("End sending data to codec\r\n")

def GetXMLDataFromCodec(codec,target):
	
	if Config.debugMode == 'True' : print("Begin getting data from codec")
	
	if (("user" in codec) & ("password" in codec)):
		authRealm = base64.b64encode(str.encode(codec["user"]+":"+codec["password"])).decode("ascii");
	else:
		authRealm = Config.endpointGenericAuthRealm
	
	conn = http.client.HTTPConnection(codec["ip"])

	if Config.debugMode == 'True' : print("Codec Target Requested :"+target)

	headers = {
		'authorization': Config.endpointGenericAuthRealm,
		'cache-control': "no-cache",
		'postman-token': "e8ea19b6-0870-01fb-dfd0-7205dfcac5cd"
		}

	try:
		conn.request("GET", "/getxml?location="+target, headers=headers)
		res = conn.getresponse()
		
	except:
		print("Error getting data from codec")
		return
		

	if Config.debugMode == 'True' : print("\r\nResponse:")
	data = res.read()
	if Config.debugMode == 'True' :  print(data.decode("utf-8"))
	return data
	if Config.debugMode == 'True' : print("End getting data to codec\r\n")