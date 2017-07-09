#!/usr/bin/env python
import json
import signal
import subprocess
import sys
import time
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
	if len(sys.argv) == 4:
		pwm_servo = sys.argv[1]
		enabServo = sys.argv[2]
		pin1Motor = sys.argv[3]
		pin2motor = sys.argv[4]
		motor_spd = sys.argv[5]
	else:
		pwm_servo = "J4.34"
		enabServo = "J4.35"
		motor_spd = "J4.36"
		pin1Motor = "J4.37"
		pin2Motor = "J4.39"
		print "Pin not properly set <servo> <enable servo> <pin1motor> <pin2motor> <enable>\nDefaults servo:PWM0:34 enabServo:35 pin1motor:PC1:37 pin2motor:PC0:39 enable:PWM1:36\n"
	print "listening on port 3000"
	node_script = subprocess.Popen(["nodejs","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	wheel = 0
	accel = 0
	time_deadzone_start = 0.0
	time_deadzone = 100.0
	try:	
		servo = PWM(pwm_servo,200)
		enable_servo = GPIO(enabServo,"OUTPUT")
		speed = PWM(motor_spd,200)
		motor1 = GPIO(pin1Motor,"OUTPUT")
		motor2 = GPIO(pin2Motor,"OUTPUT")
	except KeyError:		
		print "Invalid pin name\nFormat: J4.xx, PWMs in 34 36 38 40\n"
		sys.exit(1)
	motor1.on() #only forward, for the moment
	servo.start(0)
	speed.start(0)
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
			accel = (1-output['gamepad_z'])*50
			if output['gamepad_x'] == 0 :
				wheel = 30 #servo middle position
				time_deadzone_start = time.time()
			else:
				enable_servo.on()
				accel = accel /2 #save energy for servo, delete if we could find a way to get more amps
				wheel = ((output['gamepad_x']+1)/2*40)+10
			print int(accel)
			print int(wheel)
			if (speed > 70):
				speed.ChangeDutyCycle(int(accel))
			servo.ChangeDutyCycle(int(wheel))
			if wheel == 30:
				if time.time()-time_deadzone_start > time_deadzone: 
					enable_servo.off()
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data
