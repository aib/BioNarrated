import queue
import random
import threading
import time

import pythonosc.udp_client

def get_random_hr():
	return random.normalvariate(80, 15)

def hr_beat_thread(q, beat):
	baseline = q.get()
	while True:
		try:
			baseline = q.get(block=False)
		except queue.Empty: pass

		variance = random.normalvariate(0, 2)

		st = 60 / (baseline + variance)
		if st > 0: time.sleep(st)
		beat()

def main():
	osc_client = pythonosc.udp_client.SimpleUDPClient('10.88.0.16', 11543)
	baseline_exp = 0

	last_tick_time = time.monotonic()
	def beat():
		nonlocal last_tick_time
		now = time.monotonic()
		dt = now - last_tick_time
		last_tick_time = now

		bpm = 60 / dt
		print("tick %.2f (%.3f)" % (bpm, dt))
		osc_client.send_message('/heartbeat', bpm)

	hr_beat_queue = queue.Queue()
	threading.Thread(target=hr_beat_thread, args=(hr_beat_queue, beat)).start()

	while True:
		now = time.monotonic()

		if now > baseline_exp:
			baseline = get_random_hr()
			duration = random.normalvariate(30, 10)
			baseline_exp = now + duration
			print("Baseline now %d for %2.1fs" % (baseline, duration))
			hr_beat_queue.put(baseline)

		time.sleep(1)

if __name__ == '__main__':
	main()
