from pyparsing import Word, Literal, QuotedString, OneOrMore, srange
from pprint import pprint
#from pdb import set_trace
import sys
import board
from pdb import set_trace

__metas = [ "PB", "PW", "WR", "BR", "FF", "DT", "RE", "SZ", "KM", "TM", "OT" ]
__stones = [ "AB", "AW", "B", "W" ]
__extra = [ "C" ]

def is_meta(tag):
	return tag in __metas

def is_stone(tag):
	return tag in __stones

def is_extra(tag):
	return tag in __extra

class Node(object):
	"""this class assums that the primary property is the first one in the string.
		So files like ;C[haha]B[ab] will not work. """
	def __init__(self, name):
		self.name = name
		self.prop = ""
		self.children = []
		self.parent = None
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
		child.parent = self

	def num_child(self):
		return len(self.children)

	def has_child(self):
		return len(self.children) > 0

class SGF(object):
	def __init__(self, filename):
		#BNF
		start = Literal(";")
		text = QuotedString(quoteChar="[", 
				escChar="\\",
				multiline=True,
				unquoteResults=True,
				endQuoteChar="]")
		prop_id = Word(srange("[A-Z]"), min=1, max=2)
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

		self.reset()
	
	def reset(self):
		self.current = self.root

	def forth(self, branch=0):
		self.current = self.current.children[0]
		return self.current

	def back(self):
		self.current = self.current.parent
		return self.current

	def navigate(self):
		node = self.root
		print "Black: %s %s" % (self.info["PB"], self.info["BR"])
		print "White: %s %s" % (self.info["PW"], self.info["WR"])
		while node.has_child():
			print "%s %s [%s]" % (node.name, node.prop, node.get_comment())
			node = node.children[0]

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
