#!/usr/bin/env python
import json
import signal
import subprocess
import sys

def exit_handler(signal, frame):
	print('\nExiting...')
	node_script.terminate()
	f = open('/dev/servoblaster','w') #turn off servo
	f.write('0=0\n')
	f.close()
	servoblaster_daemon.terminate()
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)
	if len(sys.argv) > 1:
		pin = sys.argv[1]
	else:
		pin = "22"
		print "Servo pin n.22"
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	servoblaster_daemon = subprocess.Popen(["servod","--p1pins="+pin],stdout=subprocess.PIPE) #launch servoblaster
	position = "0"
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
			if output['gamepad_x'] == 0 :
				position = "50%"
			else:
				position = str((output['gamepad_x']+1)/0.02)+"%"
			f = open('/dev/servoblaster','w')
			f.write('0='+position+"\n")
			f.close()
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data
