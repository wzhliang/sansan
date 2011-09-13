#!/usr/bin/python
from pdb import set_trace


EMPTY = 0
BLACK = 1
WHITE = 2
WALL = 3

__pos = "ABCDEFGHJIKLMNOPQRST"
__num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
	12, 13, 14, 15, 16, 17, 18, 19]

__pdict = dict(zip(__pos, __num))
__ndict = dict(zip(__num, __pos))

def valid_color(color):
	return color == BLACK or color == WHITE

def str2color(s):
	if s == "B":
		return BLACK
	elif s == "W":
		return WHITE
	else:
		return 0


def pos2id(pos):
	""" convert pos like 'ab' to 1D array id"""
	x = __pdict[pos.upper()[0]]
	y = __pdict[pos.upper()[1]]
	return xy2id(x, y)

def xy2id(x, y):
	""" convert (x,y) to 1D array id"""
	return x * 19 + y

def id2xy(_id):
	""" convert id to (x,y)"""
	return divmod(_id, 19)

def id2pos(_id):
	""" convet id to 'ab' like pos """
	x, y = divmod(_id, 19)
	return __ndict[x] + __ndict[y]
	
class BoardError(Exception):
	pass

class Board(object):
	def __init__(self, size=19):
		self.size = size
		self.points = (size+2)*(size+2)
		self.data = range(self.points) # 1D array for holding stones

	def clear(self):
		for i in range(self.points):
			self.data[i] = WALL

		for i in range(20):
			for j in range(20):
				self.data[xy2id(i, j)] = EMPTY

	def valid_id(self, _id):
		#FIXME
			return True
		
	def place_stone_pos(self, pos, color):
		print "%s %d" % (pos, color)
		if pos == "":
			print "PASS"
		else:
			self.place_stone_id(pos2id(pos), color)

	def place_stone_id(self, _id, color):
		if not valid_color(color) or not self.valid_id(_id):
			raise BoardError

		if self.data[_id] != EMPTY:
			print "Warning: remove when removing stone is implemented"
			#raise BoardError

		self.data[_id] = color;
		
	

