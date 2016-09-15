from PyQt4.QtCore import pyqtRemoveInputHook
from pdb import set_trace


def debug_trace():
	'''Set a tracepoint in the Python debugger that works with Qt'''
	pyqtRemoveInputHook()
	set_trace()
