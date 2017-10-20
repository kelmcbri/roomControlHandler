 Initial Code from https://github.com/gbraux/Cisco-Showroom-RoomControl by Guillaume BRAUX
 This tweak of the original code created by Keller McBride 07/20/2017   kelmcbri@cisco.com

 Purpose:
	If more Video input sources are needed on a Cisco Video Codec, this program allows an
	external video switcher to be coupled to a port on the Cisco Video Codec.  The external
	video switcher is controlled by the Cisco Touch 10 tablet interface.

 Files:
	RoomControlHandler.py 		- Main Program.
						Launches Threaded Web Server
						Sets up new Video Sources on Cisco Video Codec
						Registers for Feedback on Inputs from Cisco Video Codec
							Re-registers for feedback periodically
	Config.py	  		- Configuration Paramters
	CondecControl.py		- Send and Receive commands for Video Codec
	ExternalHDMISwitchControl.py	- Send commands for HDMI Video Switcher
		class ESDSControl	- Serial Controller for E-SDS brand 3 port HDMI video switcher

 Components:
	E-SDS UHD 4K@60Hz HDMI Switch,3x1 HDMI Powered Switch with IR Wireless Remote, HDMI 2.0, HDCP 2.2, and RS232
		https://www.amazon.com/gp/product/B01G53WV20/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1
 	Cisco SX series Video Codec
	Controller - i.e. Server Running this python3 program - Macbook or Raspbery Pi or Cisco IR829, etc. 
