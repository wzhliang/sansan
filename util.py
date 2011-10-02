#!/usr/bin/python
from debug import debug_trace

EMPTY = 0
BLACK = 1
WHITE = 2
WALL = 3

__pos = "ABCDEFGHIJKLMNOPQRS"
__num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
	12, 13, 14, 15, 16, 17, 18, 19]

__pdict = dict(zip(__pos, __num))
__ndict = dict(zip(__num, __pos))

def valid_color(color):
	return color == BLACK or color == WHITE

def str2color(s):
	if s == "B" or s == "AB":
		return BLACK
	elif s == "W" or s == "AW":
		return WHITE
	else:
		return 0

def enemy(color):
	if color == BLACK:
		return WHITE
	elif color == WHITE:
		return BLACK
	else:
		raise IndexError

def xy2pos(x, y):
	"""convert (x,y) to 'ab' like pos"""
	return __ndict[x] + __ndict[y]

def pos2id(pos):
	"""obsolete: convert pos like 'ab' to 1D array id"""
	x = __pdict[pos.upper()[0]]
	y = __pdict[pos.upper()[1]]
	return xy2id(x, y)

def xy2id(x, y):
	"""obsolete: convert (x,y) to 1D array id"""
	return x * 19 + y

def pos2xy(pos):
	x = __pdict[pos.upper()[0]]
	y = __pdict[pos.upper()[1]]
	return (x, y)
	
def id2xy(_id):
	"""obsolete: convert id to (x,y)"""
	return divmod(_id, 19)

def id2pos(_id):
	"""obsolete: convet id to 'ab' like pos """
	x, y = divmod(_id, 19)
	return __ndict[x] + __ndict[y]

__metas = [ "PB", "PW", "WR", "BR", "FF", "DT", "RE", "SZ", "KM", "TM", "OT",
	"EV", "CA", "GM", "AP", "ST", "RU"  ]
__stones = [ "AB", "AW" ]
__extra = [ "C", "MA", "TR", "CR", "SQ", "SL", "LB" ]
__moves = [ "B", "W" ]

def is_meta(tag):
	return tag in __metas

def is_stone(tag):
	return tag in __stones

def is_move(tag):
	return tag in __moves

def is_extra(tag):
	return tag in __extra

def is_branch(tag):
	return tag in "()"

def is_node(tag):
	return tag == ";"

def is_comment(name):
	return name == "C";
	
