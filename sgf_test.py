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
		while node:
			if node.name == "B" or node.name == "W":
				self.goban.play_pos( node.prop, board.str2color(node.name) ) 
				print "##############################################"
				pprint(self.goban.data)
			else:
				print "Non stone node:"
				print node
			try:
				node = node.children[0]
			except IndexError:
				break

	#def __getattr__(self, name):
		#return super(GameGui, self).__getattr__(name)

	def navigate_back(self):
		node = None
		while True:
			self.forth()
			node = self.where()
			if is_stone(node.name):
				self.goban.play_pos( node.prop, board.str2color(node.name) ) 
				print "##############################################"
				pprint(self.goban.data)
			if not node.has_child():
				break

		while node:
			if is_stone(node.name):
				x, y = pos2xy(node.prop)
				self.goban.remove_stones([(x, y)]) 
				print "##############################################"
				print node.get_comment().decode("euc-cn")
				pprint(self.goban.data)
			node = self.back()

class GameGuiA(Game):
	def __init__(self, name, _goban):
		Game.__init__(self, name)
		self.goban = _goban
		self.build_tree()

	def find_extra(self, name):
		"Assuming no branch"
		node = self.root
		while node:
			if node.extra.has_key(name):
				print "Found ", name
				pprint(node.extra[name])
				return node.extra[name]

			try:
				node = node.children[0]
			except IndexError:
				break

		return None



class BoardTest(unittest.TestCase):
	def test_a(self):
		print "\n========= a =============\n"
		pan = Board()
		game = GameGui("sgf/kj.sgf", pan)
		game.navigate()

	def test_b(self):
		print "\n========= b =============\n"
		pan = Board()
		game = GameGui("sgf/kj.sgf", pan)
		game.navigate_back()

	def test_c(self):
		print "\n========= c =============\n"
		pan = Board()
		game = GameGui("sgf/branch.sgf", pan)
		game.navigate()

	def test_d(self):
		print "\n========= d =============\n"
		pan = Board()
		game = GameGui("sgf/branch.sgf", pan)
		for i in range(4):
			game.forth()
		self.assertEqual(game.where().num_child(), 2)
		game.forth()
		self.assertEqual(game.where().prop, "nc")
		game.branch_down()
		self.assertEqual(game.where().prop, "nd")
		game.branch_up()
		self.assertEqual(game.where().prop, "nc")

	def test_e(self):
		print "\n========= e =============\n"
		pan = Board()
		game = GameGui("sgf/bug.sgf", pan)
		game.navigate()
		pprint(pan.data)

	def test_f(self):
		print "\n========= f =============\n"
		pan = Board()
		game = GameGui("sgf/yijian-Elaure.sgf", pan)
		meta = game
		self.assertEqual(meta.PB, "Elaure")
		self.assertEqual(meta.PW, "yijian")
		self.assertEqual(meta.BR, "1k")
		self.assertEqual(meta.WR, "1k")
		self.assertEqual(meta.RE, "W+8.50")
		self.assertEqual(meta.AA, "")
		self.assertEqual(meta.BB, "")

	def test_g(self):
		print "\n========= g =============\n"
		pan = Board()
		game = GameGuiA("sgf/marks.sgf", pan)
		for n in ["TR", "MA", "CR"]:
			self.assertNotEqual(game.find_extra(n), None)

	def test_h(self):
		print "\n========= h =============\n"
		print "Test support for unexpected nodes"
		pan = Board()
		game = GameGuiA("sgf/kj1.sgf", pan)
		comment = game.find_extra("C")
		self.assertNotEqual(comment, None)
		print comment


unittest.main()
