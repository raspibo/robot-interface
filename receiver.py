#!/usr/bin/env python
import json
import signal
import subprocess
import sys
import pygame
import threading

def exit_handler(signal, frame):
	print('\nExiting...')
	Redraw.self_stopped = True
	node_script.terminate()
        pygame.quit()
	sys.exit(0)

class Redrawing(threading.Thread):
	x = y = 0
	xpaint = ypaint = 0
	def __init__(self):
		self.stopped = False
		super(Redrawing, self).__init__()

	def run(self):
		while not self.stopped:
			if self.x != 0:
				self.xpaint += self.x
			if self.y != 0:
				self.ypaint += self.y				
			screen.fill((0,255,0),(self.xpaint,self.ypaint,1,1))
			pygame.display.update()
		exit()

if __name__ == '__main__':
        pygame.init()                                           #pygame init
        screen = pygame.display.set_mode((500,500))             #same dimension as the canvas
	signal.signal(signal.SIGINT, exit_handler)
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	Redraw = Redrawing()
	Redraw.start()
	Redraw.x = Redraw.y = 0
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
			if output['device'] == "mouse":
				screen.fill((255,0,0),(output['x'],output['y'],1,1))
        	                pygame.display.update()
			elif output['device'] == "joy":
				Redraw.x = output['gamepad_x']
				Redraw.y = output['gamepad_y']
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data
