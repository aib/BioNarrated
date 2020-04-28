import time

import pythonosc.udp_client

import grovepi

def main():
	gpi = grovepi.GrovePi()
	osc = pythonosc.udp_client.SimpleUDPClient("10.88.0.16", 11543)

	prevd = False

	while True:
		d = gpi.digitalRead(7) > 0
		if not prevd and d:
			beat(osc)
		prevd = d

		time.sleep(.01)

def beat(osc):
	now = time.monotonic()
	dt = now - beat._last
	bpm = 60 / dt

	if bpm < 40:
		beat._last = now
	elif bpm > 120:
		pass
	else:
		osc.send_message('/heartbeat', bpm)
		print('/heartbeat', bpm)
		beat._last = now

beat._last = time.monotonic()

if __name__ == '__main__':
	main()
