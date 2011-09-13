from pyparsing import *
from string import lowercase
from pprint import pprint
from pdb import set_trace
import sys


class SGF:
	def __init__(self, filename):
		start = Literal(";")
		cap = lowercase.upper()
		text = QuotedString(quoteChar="[", 
				escChar="\\",
				multiline=True,
				unquoteResults=True,
				endQuoteChar="]")
		prop_id = Word(cap, min=1, max=2)
		prop = prop_id + OneOrMore(text)
		node = start + OneOrMore(prop)
		sequence = OneOrMore(node)
		branch = Literal("(") + sequence + Literal(")")
		self.game = OneOrMore( branch )

		self.meta = {}

		self.sgf_file = filename
		self.moves = None
		self.__parse()
		self.current = 0

	def next_token(self):
		tok = self.moves[self.current]
		self.current += 1
		return tok

	def __parse(self):
		fp = open(self.sgf_file)
		_all = "".join(fp)
		self.moves = self.game.parseString(_all)
		fp.close()

	def on_PB(self, current):
		self.meta["black"] = self.next_token()

	def on_PW(self, current):
		self.meta["white"] = self.next_token()

	def on_move(self, current):
		print "%s: %s" % (current, self.next_token() )

	def show(self):
		print "All moves in %s" % self.sgf_file

		set_trace()
		while True:
			try:
				current = self.next_token()
				if current == "PB":
					self.on_PB(current)
				if current == "PW":
					self.on_PW(current)
				if current == "B" or current == "W":
					self.on_move(current)
			except IndexError:
				break;

sgf = SGF(sys.argv[1])
sgf.show()

	





