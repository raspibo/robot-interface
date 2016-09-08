#!/usr/bin/env python
import json
import signal
import subprocess
import sys
import pygame

def exit_handler(signal, frame):
	print('\nExiting...')
	node_script.terminate()
        pygame.quit()
	sys.exit(0)

if __name__ == '__main__':
        pygame.init()                                           #pygame init
        screen = pygame.display.set_mode((500,500))             #same dimension as the canvas
	signal.signal(signal.SIGINT, exit_handler)
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE) #launch nodejs
	while True:
		try:
			output = json.loads(node_script.stdout.readline())             #obtain a dict from JSON
			screen.fill((255,0,0),(output['x'],output['y'],1,1))
                        #print output['x']
			#print output['y']
                        pygame.display.update()
		except ValueError:
			node_script.stdout.readline()           #discard unmeaningful data
