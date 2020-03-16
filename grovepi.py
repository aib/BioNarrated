import time

import smbus

class GrovePi:
	def __init__(self, i2c_bus=1, i2c_addr=4):
		self.bus = smbus.SMBus(i2c_bus)
		self.i2c_addr = i2c_addr
		self.retries = [0]

	def digitalRead(self, pin):
		self._write(1, [pin, 0, 0])
		data = self._read(1, 2)
		return data[1]

	def digitalWrite(self, pin, value):
		self._write(2, [pin, value, 0])
		self._read1()

	def analogRead(self, pin):
		self._write(3, [pin, 0, 0])
		data = self._read(3, 3)
		return 256 * data[1] + data[2]

	def _write(self, cmd, params):
		self._retry(lambda: self.bus.write_i2c_block_data(self.i2c_addr, cmd, params))

	def _read(self, cmd, length):
		data = self._retry(lambda: self.bus.read_i2c_block_data(self.i2c_addr, cmd, length))
		return data

	def _read1(self):
		data = self._retry(lambda: self.bus.read_byte(self.i2c_addr))
		return data

	def _retry(self, cmd):
		retries = iter(self.retries)
		while True:
			try:
				return cmd()
			except OSError as e:
				delay = next(retries, None)
				if delay is None:
					raise
				else:
					time.sleep(delay)
					continue
