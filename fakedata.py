import queue
import random
import threading
import time

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

last_tick_time = time.monotonic()
def beat():
	global last_tick_time
	now = time.monotonic()
	dt = now - last_tick_time
	last_tick_time = now
	print("tick %.2f (%.3f)" % (60/dt, dt))

def main():
	baseline_exp = 0

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
