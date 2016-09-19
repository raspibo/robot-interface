#!/usr/bin/env python
import json
import signal
import subprocess
import sys
import pygame
import threading
import time

def exit_handler(signal, frame):
	print('\nExiting...')
	Redraw.stopped = True
	node_script.terminate()
	sys.exit(0)

class Redrawing(threading.Thread):
	x = y = 0.
	xpaint = ypaint = 0.
        bounds = (0,0,0,0)

	def __init__(self):
		self.stopped = False
		super(Redrawing, self).__init__()

	def run(self):
		while not self.stopped:
			if self.x != 0:
				self.xpaint += self.x
			if self.y != 0:
				self.ypaint += self.y
                        if self.xpaint < self.bounds[0]:
                            self.xpaint = self.bounds[0]
                        elif self.xpaint > self.bounds[2]:
                            self.xpaint = self.bounds[2]
                        if self.ypaint < self.bounds[1]:
                            self.ypaint = self.bounds[1]
                        elif self.ypaint > self.bounds[3]:
                            self.ypaint = self.bounds[3]
                        screen.fill((0,255,0),(self.xpaint,self.ypaint,1,1))
                        pygame.display.update()
                pygame.quit()

if __name__ == '__main__':
        pygame.init()                                           #pygame init
        screen = pygame.display.set_mode((500,500))             #same dimension as the canvas
	signal.signal(signal.SIGINT, exit_handler)
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	Redraw = Redrawing()
	Redraw.start()
	Redraw.x = Redraw.y = 0
        Redraw.bounds = (10,10,490,490) #x min, y min, x max, y max
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
                        if output['device'] == "mouse":
                            screen.fill((255,0,0),(output['x'],output['y'],1,1))
                        elif output['device'] == "joy":
                            Redraw.x = output['gamepad_x']*0.1
                            Redraw.y = output['gamepad_y']*0.1
			#if output['device'] == "mouse":
			#	screen.fill((255,0,0),(output['x'],output['y'],1,1))
        	        #        pygame.display.update()
			#elif output['device'] == "joy":
			#	Redraw.x = output['gamepad_x']
			#	Redraw.y = output['gamepad_y']
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data
