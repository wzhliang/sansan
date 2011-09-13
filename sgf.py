from pyparsing import Word, Literal, QuotedString, OneOrMore
from string import lowercase
from pprint import pprint
#from pdb import set_trace
import sys
import board


def is_meta(tag):
	metas = [ "PB", "PW", "WR", "BR", "FF", "DT", "RE", "SZ", "KM", "TM", "OT" ]
	return tag in metas

def is_stone(tag):
	stones = [ "AB", "AW", "B", "W" ]
	return tag in stones

def is_extra(tag):
	extra = [ "C" ]
	return tag in extra

class Node(object):
	def __init__(self, name):
		self.name = name
		self.prop = ""
		self.children = []
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
		self.children.append(child)

	def num_child(self):
		return len(self.children)

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

	def show(self):
		print "All moves in %s" % self.sgf_file
		pprint(self.moves)

class Game(object):
	def __init__(self, sgf_file):
		self.sgf = SGF(sgf_file)
		self.root = Node('root')
		self.current = self.root
		self.info = {}

	def on_move(self, propid):
		node = Node(propid)
		node.set_property(self.sgf.next_token())
		self.current.add_child(node)
		self.current = node

	def on_extra(self, propid):
		self.current.add_extra(propid, self.sgf.next_token())

	def on_meta(self, propid):
		self.info[propid] = self.sgf.next_token()

	def build_tree(self):
		while True:
			try:
				current = self.sgf.next_token()
		
				if is_stone(current):
					self.on_move(current)
				elif is_meta(current):
					self.on_meta(current)
				elif is_extra(current):
					self.on_extra(current)
				else:
					pass
			except IndexError:
				break

	def navigate(self):
		node = self.root
		print "Black: %s %s" % (self.info["PB"], self.info["BR"])
		print "White: %s %s" % (self.info["PW"], self.info["WR"])
		while node.has_child():
			print "%s %s [%s]" % (node.name, node.prop, node.get_comment())
			node = node.children[0]


class GameGui(Game):
	def __init__(self, name, board):
		__super__(name)
		self.goban = board

	def navigate(self):
		node = self.root
		while node.has_child():
			if node.name == "B" or node.name == "W":
				self.goban.place_stone_pos(
					node.prop, board.str2color(node.name) ) 

			
board = Board()
game = GameGui(sys.argv[1], board)
game.build_tree()
board.clear()
game.navigate()

	





