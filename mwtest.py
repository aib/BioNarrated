import sys
import time

import NeuroSkyPy
import numpy
import pyqtgraph

def cbc(label):
	def _cb(*args, **kwargs):
		print(label, args, kwargs)
	return _cb

class Graph:
	def __init__(self):
		self.app = pyqtgraph.Qt.QtGui.QApplication([])
		self.win = pyqtgraph.GraphicsWindow()
		self.plotCount = 0
		self.plots = {}
		self.data = {}
		self.curves = {}

	def add_plot(self, label, points):
		self.plots[label] = self.win.addPlot(title=label)
		self.data[label] = numpy.zeros(points)
		self.curves[label] = self.plots[label].plot(pen="g")
		self.plotCount += 1
		if self.plotCount % 3 == 0:
			self.win.nextRow()

	def update(self, label, value):
		self.data[label] = numpy.concatenate((self.data[label][1:], numpy.array([value])))
		self.curves[label].setData(self.data[label])

	def run(self):
		pyqtgraph.Qt.QtGui.QApplication.instance().exec_()

def main():
	g = Graph()
	nsp = NeuroSkyPy.NeuroSkyPy('/dev/ttyUSB1', 115200)

	for p in ['attention', 'meditation', 'delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma', 'poorSignal', 'blinkStrength']:
		g.add_plot(p, 100)
		nsp.setCallBack(p, (lambda label: lambda v: g.update(label, v))(p))

	nsp.start()
	nsp.srl.write(b'\xc2')
	g.run()

main()
