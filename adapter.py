#!/usr/bin/python

import urllib2
from util import which
import subprocess

class AdapterError(Exception):
	pass

class Adapter(object):
	def __init__(self, source):
		self.src = source

	def adapt():
		return ""

class ExternalAdapter(Adapter):
	def __init__(self, source, exe):
		super(ExternalAdapter, self).__init__(source)
		if not exe.startswith("/") and not which(exe):
			raise AdapterError("%s not found" % exe)
		self.exe = which(exe)

	def adapt(self):
		p = subprocess.Popen([self.exe, self.src],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
		output, error = p.communicate()
		if error:
			raise AdapterError("unable to convert")

		return output

class HttpAdapter(Adapter):
	def __init__(self, source):
		super(HttpAdapter, self).__init__(source)

	def adapt(self):
		resp = urllib2.urlopen(self.src, data=None, timeout=20)
		return resp.read()
		
class PassthroughAdapter(Adapter):
	def __init__(self, source):
		super(PassthroughAdapter, self).__init__(source)

	def adapt(self):
		try:
			f = open(self.src)
			output = f.read()
			f.close()

			return output
		except IOError:
			raise

def getAdapter(fn):
	name = fn.lower()
	if name.startswith("http://"):
		return HttpAdapter(fn)
	if name.endswith(".sgf"):
		return PassthroughAdapter(fn)
	elif name.endswith(".gib"):
		return ExternalAdapter(fn, "gib2sgf")
	else:
		raise AdapterError("no suitable adapter")
