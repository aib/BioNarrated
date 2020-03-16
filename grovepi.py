import time

import smbus

class GrovePi:
	def __init__(self, i2c_bus=1, i2c_addr=4):
		self.bus = smbus.SMBus(i2c_bus)
		self.i2c_addr = i2c_addr

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
		self.bus.write_i2c_block_data(self.i2c_addr, cmd, params)
		time.sleep(.001)

	def _read(self, cmd, length):
		data = self.bus.read_i2c_block_data(self.i2c_addr, cmd, length)
		time.sleep(.001)
		return data

	def _read1(self):
		data = self.bus.read_byte(self.i2c_addr)
		time.sleep(.001)
		return data
