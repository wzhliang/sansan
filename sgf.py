from pyparsing import *
from string import lowercase
from pprint import pprint
from pdb import set_trace
import sys

class Node(object):
	def __init__(self, name):
		self.name = name
		self.children = []
		self.comment = ""
		self.prop = ""

	def set_property(self, prop):
		self.prop = prop

	def set_comment(self, comment):
		self.comment = comment

	def get_comment(self):
		return self.comment

	def add_child(self, child):
		self.children.append(child)

	def get_prop(self):
		return self.prop

	def has_child(self):
		return len(self.children) > 0

class SGF(object):
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
				break

class Game(object):
	def __init__(self, sgf_file):
		self.sgf = SGF(sgf_file)
		self.root = Node('root')
		self.current= self.root

	def on_move(self, propid):
		node = Node(propid)
		node.set_property(self.sgf.next_token())
		self.current.add_child(node)
		self.current = node

	def on_comment(self, current):
		self.current.set_comment(self.sgf.next_token())
	
	def build_tree(self):
		while True:
			try:
				current = self.sgf.next_token()
				if current == "B" or current == "W":
					self.on_move(current)
				elif current == "C":
					self.on_comment(current)
				else:
					pass
			except IndexError:
				break;

	def navigate(self):
		node = self.root
		while node.has_child():
			print "%s %s [%s]" % (node.name, node.prop, node.get_comment())
			node = node.children[0]

game = Game(sys.argv[1])
game.build_tree()
game.navigate()

	





