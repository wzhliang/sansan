#!/usr/bin/python

import unittest
from board import *
from sgf import *
from pdb import set_trace
from pprint import pprint

class GameGui(Game):
	def __init__(self, name, _goban):
		Game.__init__(self, name)
		self.goban = _goban
		self.build_tree()

	def navigate(self):
		node = self.root
		while node.has_child():
			if node.name == "B" or node.name == "W":
				self.goban.play_pos( node.prop, board.str2color(node.name) ) 
				print "##############################################"
				pprint(self.goban.data)
			node = node.children[0]

class BoardTest(unittest.TestCase):
	def test_a(self):
		print "\n========= a =============\n"
		pan = Board()
		game = GameGui("sgf/kj.sgf", pan)
		game.navigate()

unittest.main()
