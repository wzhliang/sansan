#!/usr/bin/python

import unittest
from board import *
from pdb import set_trace
from pprint import pprint

class BoardTest(unittest.TestCase):
	def test_a(self):
		print "\n=========================\n"
		pan = Board()
		pprint(pan.data)

	def test_b(self):
		print "\n=========================\n"
		pan = Board()
		pan.place_stone_xy(3, 5, WHITE)
		pprint(pan.data)
		pan.place_stone_pos("aa", BLACK)
		pprint(pan.data)

	def test_c(self):
		print "\n=========================\n"
		pan = Board()

		pan.place_stone_xy(1, 3, WHITE)
		pan.place_stone_xy(2, 3, WHITE)

		pan.place_stone_xy(1, 2, BLACK)
		pan.place_stone_xy(2, 2, BLACK)
		pan.place_stone_xy(3, 3, BLACK)
		pan.place_stone_xy(1, 4, BLACK)
		pan.place_stone_xy(2, 4, BLACK)

		pprint(pan.data)
		alive = pan.is_alive(2, 3, WHITE, [])
		self.assertEqual(alive, False)

	def test_d(self):
		print "\n=========================\n"
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
		alive = pan.is_alive(3, 3, WHITE, [])
		self.assertEqual(alive, False)

unittest.main()
