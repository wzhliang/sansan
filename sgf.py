from pyparsing import (Word, Literal, QuotedString, OneOrMore,
		srange, Forward, ZeroOrMore, Combine, Group)
from pprint import pprint
#from pdb import set_trace
import sys
import types
import board
from util import *
from pdb import set_trace

# BNF from red-bean
# 
#  Collection = GameTree { GameTree }
#  GameTree   = "(" Sequence { GameTree } ")"
#  Sequence   = Node { Node }
#  Node       = ";" { Property }
#  Property   = PropIdent PropValue { PropValue }
#  PropIdent  = UcLetter { UcLetter }
#  PropValue  = "[" CValueType "]"
#  CValueType = (ValueType | Compose)
#  ValueType  = (None | Number | Real | Double | Color | SimpleText |
#		Text | Point  | Move | Stone)

class Node(object):
	"""this class assums that the primary property is the first one in the string.
		So files like ;C[haha]B[ab] will not work. """
	def __init__(self, name):
		self.name = name
		self.prop = ""
		self.children = []
		self.parent = None
		self.prev_br = None
		self.next_br = None
		self.extra = {} # extra properties, including comment

	def set_property(self, prop):
		self.prop = prop

	def add_extra(self, name, value):
		self.extra[name] = value

	def get_comment(self):
		if self.extra.has_key("C"):
			return self.extra["C"]
		else:
			return ""

	def add_child(self, child):
		if self.num_child() > 0:
			self.children[-1].next_br = child
			child.prev_br = self.children[-1]
		self.children.append(child)
		child.parent = self

	def num_child(self):
		return len(self.children)

	def has_child(self):
		return len(self.children) > 0

	def __str__(self):
		return "%s[%s]" % (self.name, self.prop)

class SGFError(Exception):
	pass

class SGFNoMoreNode(SGFError):
	pass

class SGF(object):
	def __init__(self, filename):
		#BNF
		start = Literal(";")
		text = QuotedString(quoteChar="[", 
				escChar="\\",
				multiline=True,
				unquoteResults=True,
				endQuoteChar="]")
		prop_id = Word(srange("[A-Z]"), min=1, max=10)
		prop = prop_id + Group(OneOrMore(text))
		node = start + OneOrMore(prop)
		sequence = OneOrMore(node)
		branch = Forward()
		branch << "(" + sequence + ZeroOrMore(branch) + ")"
		self.game = OneOrMore(branch)

		self.sgf_file = filename
		self.moves = None
		self.__parse()
		self.current = 0

	def next_token(self):
		tok = self.moves[self.current]
		self.current += 1
		return tok

	def __parse(self):
		self.moves = self.game.parseFile(self.sgf_file)

	def show(self):
		print "All moves in %s" % self.sgf_file
		pprint(self.moves)

class Game(object):
	def __init__(self, sgf_file):
		self.sgf = SGF(sgf_file)
		self.root = Node('root')
		self.current = self.root
		self.info = {}
		self.stack = []

	def on_move(self, propid):
		node = Node(propid)
		node.set_property(self.sgf.next_token()[0])
		self.current.add_child(node)
		self.current = node

	def on_extra(self, propid):
		tok = self.sgf.next_token()
		if propid == "C":
			self.current.add_extra(propid, tok[0])
		else:
			self.current.add_extra(propid, tok.asList())

	def on_meta(self, propid):
		self.info[propid] = self.sgf.next_token()[0]

	def on_branch(self, br):
		if br == "(":
			self.stack.append(self.current)
		else:
			self.current = self.stack.pop()

	def build_tree(self):
		while True:
			try:
				current = self.sgf.next_token()
				pprint(current)

				if not type(current) is str:
					continue
				if is_stone(current):
					self.on_move(current)
				elif is_meta(current):
					self.on_meta(current)
				elif is_extra(current):
					self.on_extra(current)
				elif is_branch(current):
					self.on_branch(current)
				else:
					pass
			except IndexError:
				break

		self.reset()

	def reset(self):
		self.current = self.root

	def forth(self, branch=0):
		try:
			self.current = self.current.children[branch]
		except IndexError:
			raise SGFNoMoreNode

	def back(self):
		self.current = self.current.parent

	def where(self):
		return self.current

	def branch_up(self):
		"Try move up to the previous branch"
		remove = []
		node = self.current
		while node:
			remove.append(node.prop)
			if node.prev_br:
				self.current = node.prev_br
				break
			node = node.parent
		if node:
			return remove
		else:
			return []

	def branch_down(self):
		"Try move up to the previous branch"
		remove = []
		node = self.current
		while node:
			remove.append(node.prop)
			if node.next_br:
				self.current = node.next_br
				break
			node = node.parent
		if node:
			return remove
		else:
			return []

	def __getattr__(self, name):
		"Gurantteed no exception"
		if self.info.has_key(name):
			return self.info[name]
		else:
			return ""


class GameGui(Game):
	def __init__(self, name, _goban):
		Game.__init__(self, name)
		self.goban = _goban

	def navigate(self):
		node = self.root
		while node.has_child():
			if node.name == "B" or node.name == "W":
				self.goban.place_stone_pos(
					node.prop, board.str2color(node.name) ) 
			node = node.children[0]

#goban = board.Board()
#game = GameGui(sys.argv[1], goban)
#game.build_tree()
#goban.clear()
##game.navigate()
#pprint(goban.data)
