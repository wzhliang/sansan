#!/usr/bin/python

import unittest
from board import *
from pprint import pprint


class BoardTest(unittest.TestCase):
	def test_a(self):
		print "\n========= a =============\n"
		pan = Board()
		pprint(pan.data)

	def test_b(self):
		print "\n========= b =============\n"
		pan = Board()
		pan.place_stone_xy(3, 5, WHITE)
		pprint(pan.data)
		pan.place_stone_pos("aa", BLACK)
		pprint(pan.data)

	def test_c(self):
		print "\n========== c ============\n"
		pan = Board()

		pan.place_stone_xy(1, 3, WHITE)
		pan.place_stone_xy(2, 3, WHITE)

		pan.place_stone_xy(1, 2, BLACK)
		pan.place_stone_xy(2, 2, BLACK)
		pan.place_stone_xy(3, 3, BLACK)
		pan.place_stone_xy(1, 4, BLACK)
		pan.place_stone_xy(2, 4, BLACK)

		pprint(pan.data)
		clus = []
		alive = pan.is_alive(2, 3, WHITE, clus)
		self.assertEqual(alive, False)
		self.assertEqual(len(clus), 2)

	def test_d(self):
		print "\n=========== d ===========\n"
		pan = Board()

		pan.place_stone_xy(3, 3, WHITE)
		pan.place_stone_xy(4, 3, WHITE)
		pan.place_stone_xy(5, 3, WHITE)
		pan.place_stone_xy(5, 4, WHITE)

		pan.place_stone_xy(3, 2, BLACK)
		pan.place_stone_xy(4, 2, BLACK)
		pan.place_stone_xy(5, 2, BLACK)
		pan.place_stone_xy(2, 3, BLACK)
		pan.place_stone_xy(6, 3, BLACK)
		pan.place_stone_xy(3, 4, BLACK)
		pan.place_stone_xy(4, 4, BLACK)
		pan.place_stone_xy(6, 4, BLACK)
		pan.place_stone_xy(5, 5, BLACK)

		pprint(pan.data)
		clus = []
		alive = pan.is_alive(3, 3, WHITE, clus)
		self.assertEqual(alive, False)
		self.assertEqual(len(clus), 4)

	def test_e(self):
		print "\n=========== e ===========\n"
		pan = Board()

		pan.place_stone_xy(1, 2, WHITE)
		pan.place_stone_xy(1, 3, WHITE)
		pan.place_stone_xy(1, 4, WHITE)
		pan.place_stone_xy(2, 3, WHITE)

		pan.place_stone_xy(1, 1, BLACK)
		pan.place_stone_xy(1, 5, BLACK)
		pan.place_stone_xy(2, 2, BLACK)
		pan.place_stone_xy(2, 5, BLACK)
		pan.place_stone_xy(3, 3, BLACK)
		pan.place_stone_xy(3, 4, BLACK)

		print "Initial:"
		pprint(pan.data)
		alive = pan.is_alive(1, 2, WHITE, [])
		self.assertEqual(alive, True)

		print "Killing whites:"
		pan.play_xy(2, 4, BLACK)
		self.assertEqual(pan.data[1][2], EMPTY)
		self.assertEqual(pan.data[1][3], EMPTY)
		self.assertEqual(pan.data[1][4], EMPTY)
		self.assertEqual(pan.data[2][3], EMPTY)
		pprint(pan.data)

	def test_f(self):
		print "\n========== f ============\n"
		pan = Board()

		pan.place_stone_xy(1, 2, WHITE)
		pan.place_stone_xy(1, 3, WHITE)
		pan.place_stone_xy(1, 4, WHITE)
		pan.place_stone_xy(2, 3, WHITE)
		pan.place_stone_xy(2, 4, WHITE)

		pan.place_stone_xy(1, 1, BLACK)
		pan.place_stone_xy(1, 5, BLACK)
		pan.place_stone_xy(2, 2, BLACK)
		pan.place_stone_xy(2, 5, BLACK)
		pan.place_stone_xy(3, 3, BLACK)
		pan.place_stone_xy(3, 4, BLACK)

		print "Initially:"
		pprint(pan.data)
		clust = []
		alive = pan.is_alive(1, 2, WHITE, clust)
		self.assertEqual(alive, False)
		self.assertEqual(len(clust), 5)
		print "After removing 5 whites:"
		pan.remove_stones(clust)
		pprint(pan.data)

	def test_g(self):
		print "\n========= g =============\n"
		pan = Board()
		nb = pan.neighbours_pos("AA")
		self.assertEqual(len(nb), 2)
		pprint(nb)
		nb = pan.neighbours_pos("BB")
		self.assertEqual(len(nb), 4)
		pprint(nb)
		nb = pan.neighbours_pos("AB")
		self.assertEqual(len(nb), 3)
		pprint(nb)

		nb = pan.neighbours_pos("SS")
		self.assertEqual(len(nb), 2)
		pprint(nb)
		nb = pan.neighbours_pos("RR")
		self.assertEqual(len(nb), 4)
		pprint(nb)
		nb = pan.neighbours_pos("SB")
		self.assertEqual(len(nb), 3)
		pprint(nb)

	def test_h(self):
		print "\n========= h =============\n"
		pan = Board()

		pan.place_stone_xy(2, 3, WHITE)
		pan.place_stone_xy(3, 2, WHITE)
		pan.place_stone_xy(3, 4, WHITE)
		pan.place_stone_xy(4, 3, WHITE)

		pan.place_stone_xy(3, 1, BLACK)
		pan.place_stone_xy(2, 2, BLACK)
		pan.place_stone_xy(4, 2, BLACK)
		pan.place_stone_xy(1, 3, BLACK)
		pan.place_stone_xy(5, 3, BLACK)
		pan.place_stone_xy(2, 4, BLACK)
		pan.place_stone_xy(4, 4, BLACK)
		pan.place_stone_xy(3, 5, BLACK)

		print "Initially:"
		pprint(pan.data)

		pan.play_xy(3, 3, BLACK)
		self.assertEqual(pan.data[2][3], EMPTY)
		self.assertEqual(pan.data[3][2], EMPTY)
		self.assertEqual(pan.data[3][4], EMPTY)
		self.assertEqual(pan.data[4][3], EMPTY)
		print "Killing WHITEs:"
		pprint(pan.data)

	def test_i(self):
		print "\n========= i =============\n"
		pan = Board()

		pan.place_stone_xy(3, 4, WHITE)
		pan.place_stone_xy(3, 5, WHITE)
		pan.place_stone_xy(3, 6, WHITE)
		pan.place_stone_xy(4, 4, WHITE)
		pan.place_stone_xy(4, 6, WHITE)
		pan.place_stone_xy(5, 5, WHITE)

		pan.place_stone_xy(2, 4, BLACK)
		pan.place_stone_xy(2, 5, BLACK)
		pan.place_stone_xy(2, 6, BLACK)
		pan.place_stone_xy(3, 3, BLACK)
		pan.place_stone_xy(3, 7, BLACK)
		pan.place_stone_xy(4, 3, BLACK)
		pan.place_stone_xy(4, 7, BLACK)
		pan.place_stone_xy(5, 4, BLACK)
		pan.place_stone_xy(5, 6, BLACK)
		pan.place_stone_xy(6, 5, BLACK)

		print "Initially:"
		pprint(pan.data)

		pan.play_xy(4, 5, BLACK)
		self.assertEqual(pan.data[3][4], EMPTY)
		self.assertEqual(pan.data[3][5], EMPTY)
		self.assertEqual(pan.data[3][6], EMPTY)
		self.assertEqual(pan.data[4][4], EMPTY)
		self.assertEqual(pan.data[4][6], EMPTY)
		self.assertEqual(pan.data[5][5], EMPTY)
		print "Killing WHITEs:"
		pprint(pan.data)

	def test_j(self):
		print "\n========= j =============\n"
		pan = Board()

		pan.place_stone_xy(6, 19, BLACK)

		pan.place_stone_xy(5, 18, WHITE)
		pan.place_stone_xy(6, 18, WHITE)
		pan.place_stone_xy(7, 19, WHITE)

		print "Initially:"
		pprint(pan.data)

		pan.play_xy(5, 19, WHITE)
		self.assertEqual(pan.data[1][4], EMPTY)
		print "Killing WHITEs:"
		pprint(pan.data)

unittest.main()
