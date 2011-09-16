#!/usr/bin/python

import sys
import os
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pdb import set_trace
from pprint import pprint

#TODO:
# once the board is resize, everything is in a mess
# needs a bit of edge for the board.
# Stop hard-coding stone size, etc.
# Draw star, tianyuan, etc

import sgf
import board

class Bitmap:
	@staticmethod
	def get_bitmap_for_stone(color):
		if ( color == board.BLACK ):
			return "res/yun_b.png"
		else:
			return "res/yun_w.png"

	@staticmethod
	def get_bg_bitmap():
		return "background.png"

class Stone:
	"""TODO: make this a child of QGraphicsPixmapItem"""
	def __init__(self, color):
		self.color = color
		self.bitmap = QPixmap( Bitmap.get_bitmap_for_stone(color) )
		self.bitmap = self.bitmap.scaledToHeight(20)

	@staticmethod
	def get_width():
		return 20

	def get_bitmap(self):
		return self.bitmap

	def set_pos(self, pos):
		self.pos = pos

	def get_pos(self):
		return self.pos

class GoBoard(board.Board, QGraphicsView):
	def __init__(self, parent = None, size = 19):
		#TODO: how does it know to use board.Board or QGraphicsView?
		super(GoBoard, self).__init__(size)
		self.size = size
		self.w = 20
		self.h = 20
		self.edge = 25
		self.x0 = 0 + self.edge
		self.y0 = 0 + self.edge
		self.width = (self.size-1)*self.w
		self.height = (self.size-1)*self.h
		self.x1 = (self.size-1)*self.w + self.edge
		self.y1 = (self.size-1)*self.h + self.edge
		self.game = None
		self.current = None
		self.stones = [] # 2D array for holding stones (QGraphicsPixmapItem)
		for i in range(19):
			self.stones.append( [None] * 19 )

		self.scene = QGraphicsScene(0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge)
		super(QGraphicsView, self).__init__(self.scene, parent)

		self.scene.setSceneRect( 0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge )

	def set_game(self, game):
		self.game = game
		self.current = game.root

	def play_next_move(self):
		while True:
			self.current = self.current.children[0]
			print "GUI: %s %s" % (self.current.name, self.current.prop)
			if self.current.name == "B" or self.current.name == "W":
				x, y = board.pos2xy(self.current.prop)
				self.play_xy(x, y, board.str2color(self.current.name))
				break

	def mousePressEvent(self, event):
		if event.button() != Qt.LeftButton:
			return

		self.play_next_move()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Right:
			self.play_next_move()

	def mouseReleaseEvent(self, event):
		pass
		#print "mouse released ", event.button(), event.pos()

	def out_of_board(self, pix):
		x, y = pix
		if x < self.x0 or y < self.y0 or x > self.x1 or y > self.y1:
			return True
		else:
			return False

	def convert_pixel_coord(self, pix):
		if self.out_of_board( pix ):
			return (-1, -1)

		px, py = pix
		px -= self.edge
		py -= self.edge
		return  ( (px + self.w/2 )/self.w + 1, (py+self.h/2)/self.h + 1)

	def convert_coord(self, go):
		gx, gy = go
		if gx > 19 or gy > 19 or gx < 0 or gy < 0:
			return (-1, -1)

		return ((gx-1)*self.w - Stone.get_width()/2 + self.edge, 
				(gy-1)*self.w - Stone.get_width()/2 + self.edge )
	
	def draw_stars(self):
		stars = [ (4, 4), (4, 16), (16, 4), (16, 16), (10, 10) ]
		for x, y in stars:
			sx, sy = self.convert_coord((x, y))
			self.scene.addEllipse( sx, sy, 12, 12 )

	def draw_board(self):
		pen = QPen()
		pen.setWidth(2)

		# Draw background 
		bg_color = QColor(0xcb, 0x91, 0x43)
		self.scene.setBackgroundBrush(QBrush(bg_color))

		#self.draw_stars()

		# Draw frame
		rect = QRectF(self.x0, self.y0, self.x1 - self.x0,  self.y1 - self.y0)
		self.scene.addRect(rect, pen)

		# Draw lines
		for i in range(18):
			x = self.x0 + i*self.w
			y = self.y0 + i*self.h
			line = QGraphicsLineItem()
			#line.setPen( pen )
			line.setLine( x, self.y0, x,  self.y1)
			self.scene.addItem( line )

		for i in range(18):
			x = self.x0 + i*self.w
			y = self.y0 + i*self.h
			line = QGraphicsLineItem()
			#line.setPen( pen )
			line.setLine( self.x0, y, self.x1,  y )
			self.scene.addItem( line )

		self.show()

	def add_stone(self, x, y, color):
		""" Doesn't change model """
		stone = Stone(color)
		gi = QGraphicsPixmapItem(stone.get_bitmap())
		self.stones[x-1][y-1] = gi
		x, y = self.convert_coord((x, y))
		gi.setPos(x, y)
		gi.setZValue(5)
		self.scene.addItem(gi)

	def place_stone_pos(self, pos, color):
		stones = "EBW"
		try:
			super(GoBoard, self).place_stone_pos(self, pos, color)
			x, y = board.pos2xy(pos)
			self.add_stone(x, y, color)
		except board.BoardError:
			print "Failed"
			return

		stone = Stone(stones[color])
		gi = self.scene.addPixmap( stone.get_bitmap() )
		gi.setZValue( self._stone_zvalue )
		x, y = self.convert_coord( board.pos2xy(pos) )
		gi.setPos( x, y )
		return gi

	def remove_stone(self, xy):
		print "remove_stone: removing ", item
		x, y = xy
		print "remove_stone: pos ", board.xy2pos(x, y)
		gi = self.stones.pop( board.xy2pos(x, y) )
		self.scene.removeItem( gi )

	def delShadedStone(self):
		print "delShadedStone() stubbed"

	def play(self, pos, color=None):
		""" Play a stone of color (default is self.currentColor) at pos. """
		if color is None:
			color = self.currentColor
		if abstractBoard.play(self, pos, color):					# legal move?
			captures = self.undostack[len(self.undostack)-1][2]	 # retrieve list of captured stones
			print "captures: ", captures
			for x in captures:
				self.remove_stone( self.stone[x] )
			self.place_stone(pos, color)
			self.currentColor = self.invert(color)
			self.delShadedStone()
			return 1
		else: return 0

	def clear(self):
			print "Failed to place stone"
			pass

	def remove_stone(self, x, y):
		gi = self.stones[x-1][y-1]
		self.scene.removeItem(gi)

	def play_xy(self, x, y, color):
		try:
			dead = super(GoBoard, self).play_xy(x, y, color)
			# Add only as the model knows about this new stone
			self.add_stone(x, y, color)
			for dx, dy in dead:
				self.remove_stone(dx, dy)
		except IndexError:
			print "Unable to make move: (%d,%d,%d)" % (x, y, color)
			# Remove the just played stone
			pass

	def _clear(self):
		#TODO: remove existing stones
		#TODO: might need a modified flag
		#print "GoBoard: number of stones on board: ", len( self.stones_gi )
		
		# Clearing all current stuff TODO: refresh the board instead.
		#set_trace()
		#for gi in self.scene.items():
			#self.scene.removeItem(gi)

		self.draw_board()

	def setup(self):
		self.clear()

class MyWidget(QWidget):
	def __init__(self, parent = None):
		super(MyWidget, self ).__init__(parent)

		self.goban = GoBoard(self)
		self.goban.draw_board()

		self.game = sgf.Game(sys.argv[1])
		self.game.build_tree()

		self.goban.set_game( self.game )
		self.goban.setup()


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.widget = MyWidget()
		self.setCentralWidget(self.widget)

		self.createActions()
		self.createMenus()

		self.setWindowTitle("SIHUO")

	def open(self):
		print "Invoked <b>File|Open</b>"

	def next(self):
		print 'Move to next'
		self.widget.next()

	def reset(self):
		print 'Reset'
		self.widget.goban.clear()

	def undo(self):
		print "Invoked <b>Edit|Undo</b>"

	def redo(self):
		print "Invoked <b>Edit|Redo</b>"

	def about(self):
		QMessageBox.about(self, "About Menu",
				"The <b>Menu</b> example shows how to create menu-bar menus "
				"and context menus.")

	def aboutQt(self):
		print "Invoked <b>Help|About Qt</b>"

	def createActions(self):
		self.openAct = QAction("&Open...", self,
				shortcut=QKeySequence.Open,
				statusTip="Open an existing file", triggered=self.open)

		self.nextAct = QAction("&Next...", self,
				shortcut= QKeySequence( "Ctrl-N" ),
				statusTip="Go to next problem", triggered=self.next)

		self.resetAct = QAction("&Restart...", self,
				shortcut= QKeySequence( "Ctrl-R" ),
				statusTip="Rstart problem solving", triggered=self.reset)

		self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
				statusTip="Exit the application", triggered=self.close)

		self.undoAct = QAction("&Undo", self,
				shortcut=QKeySequence.Undo,
				statusTip="Undo the last operation", triggered=self.undo)

		self.redoAct = QAction("&Redo", self,
				shortcut=QKeySequence.Redo,
				statusTip="Redo the last operation", triggered=self.redo)

		self.aboutAct = QAction("&About", self,
				statusTip="Show the application's About box",
				triggered=self.about)

		self.aboutQtAct = QAction("About &Qt", self,
				statusTip="Show the Qt library's About box",
				triggered=self.aboutQt)
		self.aboutQtAct.triggered.connect(qApp.aboutQt)

	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.nextAct)
		self.fileMenu.addAction(self.resetAct)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)

		self.helpMenu = self.menuBar().addMenu("&Help")
		self.helpMenu.addAction(self.aboutAct)
		self.helpMenu.addAction(self.aboutQtAct)

# MAIN MAIN MAIN ######################################
app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.resize( 460, 460 )
sys.exit(app.exec_())

