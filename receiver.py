#!/usr/bin/env python
import json
import signal
import subprocess
import sys

def exit_handler(signal, frame):
	print('\nExiting...')
	node_script.terminate()
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, exit_handler)
	node_script = subprocess.Popen(["node","interface.js"],stdout=subprocess.PIPE)
	while True:
		try:
			output = json.loads(node_script.stdout.readline())
			print output['x']
			print output['y']
		except ValueError:
			not_json = node_script.stdout.readline()
			if not_json != "":
				print not_json
