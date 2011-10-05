#!/usr/bin/python

import sys
import os
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pprint import pprint

#TODO:
# once the board is resize, everything is in a mess
# needs a bit of edge for the board.
# Stop hard-coding stone size, etc.
# Draw star, tianyuan, etc

from util import *
from debug import debug_trace
import sgf
import board

class Bitmap:
	@staticmethod
	def get_bitmap_for_stone(color):
		if ( color == BLACK ):
			return "res/b22.png"
		else:
			return "res/208.png"

	@staticmethod
	def get_bg_bitmap():
		return "background.png"

class Stone:
	"""TODO: make this a child of QGraphicsPixmapItem"""
	def __init__(self, color):
		self.color = color
		self.bitmap = QPixmap( Bitmap.get_bitmap_for_stone(color) )
		self.bitmap = self.bitmap.scaledToHeight(38, mode=1)

	@staticmethod
	def get_width():
		return 40

	def get_bitmap(self):
		return self.bitmap

	def set_pos(self, pos):
		self.pos = pos

	def get_pos(self):
		return self.pos

class Cross(QGraphicsItem):
	"Indicator of the current stone"
	Type = QGraphicsItem.UserType + 2

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Cross, self).__init__()

		self.size = size
		self.point = point
		self.topLeft = QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(Qt.NoButton)
		#self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Cross.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0*self.size, 2.0*self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		line = QLineF(self.point.x() - self.size, self.point.y(),
			self.point.x() + self.size, self.point.y())

		if line.length() == 0.0:
			return

		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QLineF(self.point.x(), self.point.y() + self.size,
			self.point.x(), self.point.y() - self.size)

		if line.length() == 0.0:
			return

		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
				Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

class Square(QGraphicsItem):
	"square mark"
	Type = QGraphicsItem.UserType + 3

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Square, self).__init__()

		self.size = size
		self.point = point
		self.topLeft = QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(Qt.NoButton)
		#self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Square.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0*self.size, 2.0*self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		x1 = self.point.x() - self.size
		x2 = self.point.x() + self.size
		y1 = self.point.y() - self.size
		y2 = self.point.y() + self.size

		line = QLineF(x1, y1, x1, y2)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)
	
		line = QLineF(x1, y1, x2, y1)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QLineF(x2, y1, x2, y2)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)
	
		line = QLineF(x2, y2, x1, y2)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

class Triangle(QGraphicsItem):
	"trangle mark"
	Type = QGraphicsItem.UserType + 4

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Triangle, self).__init__()

		self.size = size
		self.point = point
		self.topLeft = QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(Qt.NoButton)
		#self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Triangle.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0*self.size, 2.0*self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		x1 = self.point.x() - self.size
		x2 = self.point.x() + self.size
		y1 = self.point.y() - self.size
		y2 = self.point.y() + self.size

		line = QLineF(x1, y1, x1, y2)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)
	
		line = QLineF(x1, y1, x2, y1)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QLineF(x1, y1, x2, y2)
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

class Circle(QGraphicsItem):
	"circle mark"
	Type = QGraphicsItem.UserType + 5

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Circle, self).__init__()

		self.size = size
		self.point = point

		self.setAcceptedMouseButtons(Qt.NoButton)
		#self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0*self.size, 2.0*self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)

class Mark(QGraphicsItem):
	"generic mark"
	Type = QGraphicsItem.UserType + 6

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Mark, self).__init__()

		self.size = size
		self.point = point

		self.setAcceptedMouseButtons(Qt.NoButton)
		#self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0*self.size, 2.0*self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		painter.setPen(QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)


class GoBoard(board.Board, QGraphicsView):
	def __init__(self, parent = None, size = 19):
		#TODO: how does it know to use board.Board or QGraphicsView?
		super(GoBoard, self).__init__(size)
		self.size = size
		self.w = 40
		self.h = 40
		self.edge = 30
		self.x0 = 0 + self.edge
		self.y0 = 0 + self.edge
		self.width = (self.size-1)*self.w
		self.height = (self.size-1)*self.h
		self.x1 = (self.size-1)*self.w + self.edge
		self.y1 = (self.size-1)*self.h + self.edge
		self.game = None
		self.stones = [] # 2D array for holding stones (QGraphicsPixmapItem)
		self.marks = [] # 2D array for hodling various marks
		self.cross = None
		for i in range(19):
			self.stones.append([None] * 19)

		self.scene = QGraphicsScene(0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge)
		super(QGraphicsView, self).__init__(self.scene, parent)

		self.scene.setSceneRect( 0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge )

	def set_game(self, game):
		self.game = game

	def go_next(self):
		try:
			self.game.forth()
		except sgf.SGFNoMoreNode:
			print "End of game or branch."
			return
		print "GUI: %s" % (self.game.where())
		self.handle_node(self.game.where())

	def go_prev(self):
		# TODO: should put back the deaad stones
		x, y = pos2xy(self.game.where().prop)
		self.remove_stone(x, y)
		super(GoBoard, self).remove_stones([(x, y)])
		self.game.back()
		self.handle_node(self.game.where(), True)
		#TODO: The following causes exception of cause (place occupied) but not
		#sure if there is situation where going back will kill some stones
		#if is_move(self.game.where().name):
		#	self.handle_move(self.game.where())

	def handle_node(self, node, back=0):
		"Handle a node, like mark, comment, etc. dead stone is not handled here"
		self.emit(SIGNAL("newComment(PyQt_PyObject)"), "")
		self.clear_marks()
		if is_stone(node.name):
			self.handle_stone(node)
		# When going back, the stone is already there
		elif is_move(node.name):
			if not back:
				self.handle_move(node)
			self.refresh_cross(node)

		for e in node.extra:
			print "Handling %s..." % e, node.extra[e]
			if is_comment(e):
				self.emit(SIGNAL("newComment(PyQt_PyObject)"), node.get_comment())
			elif e == "LB":
				self._handle_LB(node.extra[e])
			elif e == "CR":
				self._handle_CR(node.extra[e])
			elif e == "SQ":
				self._handle_SQ(node.extra[e])
			elif e == "TR":
				self._handle_TR(node.extra[e])
			elif e == "MA":
				self._handle_MA(node.extra[e])

	def clear_marks(self):
		"""Assuming that marks are only relavant for a particular move and ALL should be
		cleared from board"""
		while True:
			try:
				self.scene.removeItem(self.marks.pop())
			except IndexError:
				break

	def refresh_cross(self, node):
		if self.cross:
			self.scene.removeItem(self.cross)
		x, y = pos2xy(self.game.where().prop)
		cx, cy = self.convert_coord((x, y))
		self.cross = Cross(QPointF(cx, cy), 10)
		self.cross.setZValue(10)
		self.scene.addItem(self.cross)

	def handle_move(self, node):
		"Handle a move. Deal with dead stone, etc. Assuming it's a play node"
		if node.prop == "":
			print "PASS"
			self.emit(SIGNAL("newComment(PyQt_PyObject)"), "PASS")
		else:
			x, y = pos2xy(self.game.where().prop)
			self.play_xy(x, y, str2color(self.game.where().name))

	def handle_stone(self, node):
		for l in node.prop:
			print "Placing stone at %s" % l
			x, y = pos2xy(l)
			self.add_stone(x, y, str2color(node.name))

	def _handle_LB(self, labels):
		for l in labels:
			pos, char = l.split(":")
			x, y = pos2xy(pos)
			self.add_label(x, y, char)

	def _handle_CR(self, locs):
		for l in locs:
			x, y = pos2xy(l)
			self.add_circle(x, y, 10)

	def _handle_TR(self, locs):
		for l in locs:
			x, y = pos2xy(l)
			self.add_triangle(x, y, 10)

	def _handle_SQ(self, locs):
		for l in locs:
			x, y = pos2xy(l)
			self.add_square(x, y, 10)

	def _handle_MA(self, locs):
		for l in locs:
			x, y = pos2xy(l)
			self.add_mark(x, y, 10)

	def _remove_stones(self, group):
		remove = []
		for prop in group:
			x, y = pos2xy(prop)
			self.remove_stone(x, y)
			remove.append((x,y))
		super(GoBoard, self).remove_stones(remove)

	def go_up(self):
		"Go up in variantions"
		remove = self.game.branch_up()
		if len(remove) == 0:
			return
		self._remove_stones(remove)
		self.handle_node(self.game.where())

	def go_down(self):
		"Go up in variantions"
		remove = self.game.branch_down()
		if len(remove) == 0:
			return
		self._remove_stones(remove)
		self.handle_node(self.game.where())

	def mousePressEvent(self, event):
		if event.button() != Qt.LeftButton:
			return
		self.go_next()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Right:
			self.go_next()
		elif event.key() == Qt.Key_Left:
			self.go_prev()
		elif event.key() == Qt.Key_Up:
			self.go_up()
		elif event.key() == Qt.Key_Down:
			self.go_down()

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
		"convert stone logical position into pixel postion"
		gx, gy = go
		if gx > 19 or gy > 19 or gx < 0 or gy < 0:
			return (-1, -1)

		return ((gx-1)*self.w +  self.edge, 
				(gy-1)*self.w + self.edge )
	
	def draw_stars(self):
		stars = [ (4, 4), (4, 16), (16, 4), (16, 16), (10, 10) ]
		for x, y in stars:
			sx, sy = self.convert_coord((x, y))
			sx -= 4
			sy -= 4
			self.scene.addEllipse(sx, sy, 8, 8, brush = QBrush(Qt.black))

	def draw_board(self):
		pen = QPen()
		pen.setWidth(2)

		# Draw background 
		bg_color = QColor(0xcb, 0x91, 0x43)
		self.scene.setBackgroundBrush(QBrush(bg_color))

		self.draw_stars()

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

		self.setRenderHint(QPainter.Antialiasing)
		self.scale(0.8, 0.8)
		self.show()

	def add_stone(self, x, y, color):
		""" Doesn't change model """
		stone = Stone(color)
		gi = QGraphicsPixmapItem(stone.get_bitmap())
		self.stones[x-1][y-1] = gi
		x, y = self.convert_coord((x, y))
		x -= 0.5*self.w # FIXME: somehow, this is in the middle
		y -= 0.5*self.w
		gi.setPos(x, y)
		#gi.setZValue(5)

		effect = QGraphicsDropShadowEffect(self)
		effect.setBlurRadius(1)
		effect.setOffset(3.0)
		gi.setGraphicsEffect(effect)

		self.scene.addItem(gi)

	def add_label(self, x, y, char):
		""" Doesn't change model """
		gi = self.scene.addText(char)
		self.marks.append(gi) # overwriting previous one. should be GCed automatically
		x, y = self.convert_coord((x, y))
		x -= 0.2*self.w # FIXME: hard-coded location
		y -= 0.2*self.w
		gi.setPos(x, y)
		gi.setZValue(5)

	def add_circle(self, x, y, size):
		x, y = self.convert_coord((x, y))
		cr = Circle(QPointF(x, y), size)
		cr.setZValue(5)
		self.marks.append(cr)
		self.scene.addItem(cr)

	def add_triangle(self, x, y, size):
		x, y = self.convert_coord((x, y))
		tr = Triangle(QPointF(x, y), size)
		tr.setZValue(5)
		self.marks.append(tr)
		self.scene.addItem(tr)

	def add_square(self, x, y, size):
		x, y = self.convert_coord((x, y))
		sq = Square(QPointF(x, y), size)
		sq.setZValue(5)
		self.marks.append(sq)
		self.scene.addItem(sq)

	def add_mark(self, x, y, size):
		x, y = self.convert_coord((x, y))
		ma = Mark(QPointF(x, y), size)
		ma.setZValue(5)
		self.marks.append(ma)
		self.scene.addItem(ma)

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

		layout = QVBoxLayout()
		layout.addWidget(self.goban)
		self.setLayout(layout)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.widget = MyWidget()
		self.setCentralWidget(self.widget)

		self.createActions()
		self.createMenus()
		self.createDockWindows()

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

	def populateGameInfo(self):
		meta = self.widget.game
		self.gameInfoEdit.append("BLACK: " + meta.PB.decode("euc-cn")
			+ " " + meta.BR.decode("euc-cn"))
		self.gameInfoEdit.append("WHITE: " + meta.PW.decode("euc-cn")
			+ " " + meta.WR.decode("euc-cn"))
		self.gameInfoEdit.append("RESULT: " + meta.RE.decode("euc-cn"))

	def displayComment(self, comment):
		self.commentEdit.clear()
		self.commentEdit.append(comment.decode("euc-cn"))

	def createDockWindows(self):
		dock = QDockWidget("Game Info", self)
		dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
		self.gameInfoEdit = QTextEdit()
		dock.setWidget(self.gameInfoEdit)
		self.addDockWidget(Qt.RightDockWidgetArea, dock)
		self.populateGameInfo()
		#self.viewMenu.addAction(dock.toggleViewAction())

		dock = QDockWidget("Comment", self)
		self.commentEdit = QTextEdit()
		dock.setWidget(self.commentEdit)
		self.addDockWidget(Qt.RightDockWidgetArea, dock)
		#self.viewMenu.addAction(dock.toggleViewAction())


		self.connect(self.widget.goban, SIGNAL("newComment(PyQt_PyObject)"), self.displayComment)
		#self.customerList.currentTextChanged.connect(self.insertCustomer)
		#self.paragraphsList.currentTextChanged.connect(self.addParagraph)

# MAIN MAIN MAIN ######################################
app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.resize( 920, 920 )
sys.exit(app.exec_())

