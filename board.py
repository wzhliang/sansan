#!/usr/bin/python


EMPTY = 0
BLACK = 1
WHITE = 2
WALL = 3

__pos = "ABCDEFGHJKLMNOPQRST"
__num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
	12, 13, 14, 15, 16, 17, 18, 19]

__pdict = zip(__pos, __num)
__ndict = zip(__num, __pos)

def valid_color(color):
	return color == BLACK or color == WHITE

def str2color(str):
	if str == "B":
		return BLACK
	elif str == "W":
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
	
class Board(object):
	def __init__(self, size=19):
		self.size = size
		self.data = [] # 1D array for stones
		self.points = (size+2)*(size+2)

	def clear(self):
		for i in range(self.points):
			self.data[i] = WALL

		for i in range(20):
			for j in range(20):
				self.data[xy2id(i, j)] = EMPTY

	def valid_id(self, id):
		x, y = id2xy(id)
		if x == 0 or y == 0 or x == 20 or y == 20:
			return False
		else:
			return True
		
	def place_stone_pos(self, pos, color):
		self.place_stone_id(pos2id(pos), color)

	def place_stone_id(self, _id, color):
		if !valid_color(color) or ! self.valid_id(_id):
			raise BoardError

		if self.data[_id] != EMPTY:
			raise BoardError

		self.data[_id] = color;
		
	

