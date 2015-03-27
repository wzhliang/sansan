#!/usr/bin/python

import unittest
from board import *
from sgf import *
from pprint import pprint

class GameGui(Game):
	def __init__(self, name, _goban):
		f = open(name, "rt")
		content = f.read()
		f.close()
		Game.__init__(self, content)
		self.goban = _goban
		self.build_tree()

	def navigate(self):
		node = self.root
		while node:
			if node.name == "B" or node.name == "W":
				print "##############################################"
				self.goban.play_pos( node.prop, board.str2color(node.name) ) 
				pprint(self.goban.data)
			else:
				print "Non stone node:", node
			try:
				node = node.children[0]
			except IndexError:
				print "Node has no child"
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
		f = open(name, "rt")
		content = f.read()
		f.close()
		Game.__init__(self, content)
		self.goban = _goban
		self.build_tree()

	def find_extra(self, name):
		"Assuming no branch"
		node = self.root
		while node:
			if node.extra.has_key(name):
				print "Found ", name
				pprint(node.extra[name])
				return node

			try:
				node = node.children[0]
			except IndexError:
				break

		return None


class BoardTest(unittest.TestCase):
	def test_a(self):
		print "\n========= TEST a =============\n"
		pan = Board()
		game = GameGui("sgf/kj.sgf", pan)
		game.navigate()

	def test_b(self):
		print "\n========= TEST b =============\n"
		pan = Board()
		game = GameGui("sgf/kj.sgf", pan)
		game.navigate_back()

	def test_c(self):
		print "\n========= TEST c =============\n"
		pan = Board()
		game = GameGui("sgf/branch.sgf", pan)
		game.navigate()

	def test_d(self):
		print "\n========= TEST d =============\n"
		pan = Board()
		game = GameGui("sgf/branch.sgf", pan)
		for i in range(5):
			game.forth()
		self.assertEqual(game.where().prop, "nc")
		game.branch_down()
		self.assertEqual(game.where().prop, "nd")
		game.branch_up()
		self.assertEqual(game.where().prop, "nc")

	def test_e(self):
		print "\n========= TEST e =============\n"
		pan = Board()
		game = GameGui("sgf/bug.sgf", pan)
		game.navigate()
		pprint(pan.data)

	def test_f(self):
		print "\n========= TEST f =============\n"
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
		print "\n========= TEST g =============\n"
		pan = Board()
		game = GameGuiA("sgf/marks.sgf", pan)
		for n in ["TR", "MA", "CR"]:
			self.assertNotEqual(game.find_extra(n), None)

	def test_h(self):
		print "\n========= TEST h =============\n"
		print "Test support for comment in the first node as most tom qipu does"
		pan = Board()
		game = GameGuiA("sgf/kj1.sgf", pan)
		node = game.find_extra("C")
		self.assertNotEqual(node, None)
		print node.get_comment()

	def test_i(self):
		print "\n========= TEST i =============\n"
		print "Test support for strange node where move property is in the middle"
		pan = Board()
		game = GameGuiA("sgf/strange.sgf", pan)
		node = game.find_extra("C")
		self.assertNotEqual(node, None)
		self.assertEqual(node.get_comment().startswith("Elaure"), True)
		self.assertEqual(node.name, "B")
		self.assertEqual(node.prop, "pd")

	def test_j(self):
		print "\n========= TEST j =============\n"
		print "Test presentable()"
		pan = Board()
		game = GameGuiA("sgf/marks.sgf", pan)
		good = False
		while True:
			try:
				game.forth()
			except SGFNoMoreNode:
				break
			if game.where().presentable():
				good = True
				break
		self.assertEqual(good, True)

	def test_k(self):
		print "\n========= TEST k =============\n"
		print "Test support for PB, PW nodes."
		pan = Board()
		game = GameGui("sgf/place.sgf", pan)
		game.forth()
		self.assertEqual(game.where().name, "AB")
		pprint(game.where().prop)
		self.assertEqual(len(game.where().prop), 4)
		self.assertTrue("aa" in game.where().prop)
		self.assertTrue("bb" in game.where().prop)
		game.forth()
		self.assertEqual(game.where().name, "AW")
		pprint(game.where().prop)
		self.assertEqual(len(game.where().prop), 4)
		self.assertTrue("gg" in game.where().prop)
		self.assertTrue("ef" in game.where().prop)

	def test_l(self):
		print "\n========= TEST l =============\n"
		print "Test support non-std pandago property"
		pan = Board()
		game = GameGui("sgf/pandago.sgf", pan)
		game.navigate()

unittest.main()
