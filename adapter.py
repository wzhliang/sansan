#!/usr/bin/python

import urllib2
from util import which
import subprocess
import re


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


class SinaAdapter(HttpAdapter):
	"""javascript:gibo_load('http://duiyi.sina.com.cn/cgibo/foo.sgf')"""
	def __init__(self, source):
		pat = re.compile("gibo_load\('(.*)'\)")
		matobj = pat.search(source)
		print matobj.group(1)
		if matobj is None:
			raise AdapterError("Not a sina qipu address")
		super(SinaAdapter, self).__init__(matobj.group(1))


class UgiAdapter(Adapter):
	def __init__(self, source):
		super(UgiAdapter, self).__init__(source)
		self.pat = re.compile("^([A-Z][A-Z]),([BW])1,\d+,\d+$")

	def adapt(self):
		with open(self.src) as f:
			return self._adapt(f)

	def convert_move(self, l):
		matobj = self.pat.match(l)
		if matobj is None:
			return ""
		return ";%s[%s]" % (matobj.group(2), matobj.group(1))

	def _adapt(self, f):
		sgf = "(;FF[4]"
		for l in f:
			sgf = sgf + self.convert_move(l.strip())
		sgf = sgf + ")"
		return sgf


class HttpUgiAdapter(UgiAdapter):
	def __init__(self, source):
		super(HttpUgiAdapter, self).__init__(source)

	def adapt(self):
		sgf = "(;FF[4]"
		resp = urllib2.urlopen(self.src, data=None, timeout=20)
		for l in resp.readlines():
			sgf = sgf + self.convert_move(l.strip())
		sgf = sgf + ")"
		return sgf


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
	if "duiyi.sina" in name:
		return SinaAdapter(fn)
	if name.startswith("http://") and name.endswith(".ugi"):
		return HttpUgiAdapter(fn)
	if name.startswith("http://"):
		return HttpAdapter(fn)
	if name.endswith(".sgf"):
		return PassthroughAdapter(fn)
	elif name.endswith(".gib"):
		return ExternalAdapter(fn, "gib2sgf")
	elif name.endswith(".ugi"):
		return UgiAdapter(fn)
	else:
		raise AdapterError("no suitable adapter")
