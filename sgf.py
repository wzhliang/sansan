from pyparsing import *
from string import lowercase
from pprint import pprint
from pdb import set_trace
import sys

class SGF:
	def __init__(self, filename):
		start = ";"
		stone = Word("BW")
		pos = Word(lowercase, exact=2)
		self.play = start + stone + "[" + pos + "]"

		self.sgf_file = filename
		self.moves=[]

		self.__parse()

	def __parse(self):
		fp = open(self.sgf_file)
		for l in fp:
			try:
				move = self.play.parseString(l)
				self.moves.append(move)
			except:
				print "Can't handle line %s." % l
		fp.close()

	def show(self):
		print "All moves in %s" % self.sgf_file
		for m in self.moves:
			print m[1], m[3]


sgf = SGF(sys.argv[1])
sgf.show()

	





