#!/usr/bin/env python
import json
import signal
import subprocess
import sys
from acmepins import GPIO
from acmepins import PWM


def exit_handler(signal, frame):
	print('\nExiting...')
	node_script.terminate()
	servo.stop()
	speed.stop()
	motor1.off()
	motor2.off()
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)
	if len(sys.argv) > 4:
		try:
			pwm_servo = sys.argv[1]
			pin1Motor = sys.argv[2]
			pin2motor = sys.argv[3]
			motor_spd = sys.argv[4]
		except KeyError:
			print "Invalid pin name\nFormat: J4.xx, PWMs in 34 36 38 40\n"
			sys.exit(0)
	else:
		pwm_servo = "J4.34"
		motor_spd = "J4.36"
		pin1Motor = "J4.37"
		pin2Motor = "J4.39"
		print "Pin not properly setted <servo> <pin1motor> <pin2motor> <enable>\nDefaults servo:PWM0:34 pin1motor:PC1:37 pin2motor:PC0:39 enable:PWM1:36\n"
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	position = "0"
	servo = PWM(pwm_servo,200)
	speed = PWM(motor_spd,200)
	motor1 = GPIO(pin1Motor,"OUTPUT")
	motor2 = GPIO(pin2Motor,"OUTPUT")
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
			if output['gamepad_x'] == 0 :
				position = "50%"
			else:
				position = str((output['gamepad_x']+1))
			#f = open('/dev/servoblaster','w')
			#f.write('0='+position+"\n")
			#f.close()
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data