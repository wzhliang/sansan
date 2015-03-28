#!/usr/bin/python

import sys
import math
import functools
from PyQt4 import QtCore
from PyQt4 import QtGui

# TODO:
# once the board is resize, everything is in a mess
# needs a bit of edge for the board.
# Stop hard-coding stone size, etc.

import util
import sgf
import board
import adapter
from wq_rc import *


class Bitmap:
	@staticmethod
	def get_bitmap_for_stone(color):
		if (color == util.BLACK):
			return ":res/b22.png"
		else:
			return ":res/208.png"

	@staticmethod
	def get_bg_bitmap():
		return "background.png"


class Stone:
	"""TODO: make this a child of QGraphicsPixmapItem"""
	def __init__(self, color):
		self.color = color
		self.bitmap = QtGui.QPixmap(Bitmap.get_bitmap_for_stone(color))
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


class Cross(QtGui.QGraphicsItem):
	"Indicator of the current stone"
	Type = QtGui.QGraphicsItem.UserType + 2

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Cross, self).__init__()

		self.size = size
		self.point = point
		self.topLeft = QtCore.QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Cross.Type

	def boundingRect(self):
		return QtCore.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		line = QtCore.QLineF(self.point.x() - self.size, self.point.y(),
			self.point.x() + self.size, self.point.y())

		if line.length() == 0.0:
			return

		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(self.point.x(), self.point.y() + self.size,
			self.point.x(), self.point.y() - self.size)

		if line.length() == 0.0:
			return

		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)


class Square(QtGui.QGraphicsItem):
	"square mark"
	Type = QtGui.QGraphicsItem.UserType + 3

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Square, self).__init__()

		self.size = size
		self.point = point
		self.topLeft = QtGui.QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Square.Type

	def boundingRect(self):
		return QtGui.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		x1 = self.point.x() - self.size
		x2 = self.point.x() + self.size
		y1 = self.point.y() - self.size
		y2 = self.point.y() + self.size

		line = QtGui.QLineF(x1, y1, x1, y2)
		painter.setPen(QtGui.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QtGui.QLineF(x1, y1, x2, y1)
		painter.setPen(QtGui.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QtGui.QLineF(x2, y1, x2, y2)
		painter.setPen(QtGui.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)

		line = QtGui.QLineF(x2, y2, x1, y2)
		painter.setPen(QtGui.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawLine(line)


class Triangle(QtGui.QGraphicsItem):
	"trangle mark"
	Type = QtGui.QGraphicsItem.UserType + 4

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Triangle, self).__init__()

		self.size = size
		self.point = point

		self.setAcceptedMouseButtons(Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Triangle.Type

	def boundingRect(self):
		return QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		x1 = self.point.x()
		y1 = self.point.y() - self.size
		x2 = self.point.x() - abs(self.size * math.sin(30))
		y2 = self.point.y() + self.size * math.cos(30)
		x3 = self.point.x() + abs(self.size * math.sin(30))

		line = QtGui.QLineF(x1, y1, x2, y2)
		painter.setPen(QtGui.QPen(Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtGui.QLineF(x2, y2, x3, y2)
		painter.setPen(QtGui.QPen(Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtGui.QLineF(x1, y1, x3, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)


class Circle(QtGui.QGraphicsItem):
	"circle mark"
	Type = QtGui.QGraphicsItem.UserType + 5

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Circle, self).__init__()

		self.size = size
		self.point = point

		self.setAcceptedMouseButtons(Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QtGui.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		painter.setPen(QtCore.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)


class Mark(QtGui.QGraphicsItem):
	"generic mark"
	Type = QtGui.QGraphicsItem.UserType + 6

	def __init__(self, point, size):
		"point: QPointF object as I don't know the board"
		super(Mark, self).__init__()

		self.size = size
		self.point = point

		self.setAcceptedMouseButtons(Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QtGui.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		painter.setPen(QtCore.QPen(Qt.red, 3, Qt.SolidLine,
			Qt.RoundCap, Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)


class GoBoard(board.Board, QtGui.QGraphicsView):
	def __init__(self, parent=None, size=19):
		# TODO: how does it know to use board.Board or QGraphicsView?
		super(GoBoard, self).__init__(size)
		self.size = size
		self.w = 40
		self.h = 40
		self.edge = 30
		self.x0 = 0 + self.edge
		self.y0 = 0 + self.edge
		self.width = (self.size - 1) * self.w
		self.height = (self.size - 1) * self.h
		self.x1 = (self.size - 1) * self.w + self.edge
		self.y1 = (self.size - 1) * self.h + self.edge
		self.game = None
		self.stones = []  # 2D array for holding stones (QGraphicsPixmapItem)
		self.marks = []  # 2D array for hodling various marks
		self.cross = None
		for i in range(19):
			self.stones.append([None] * 19)

		self.scene = QtGui.QGraphicsScene(0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge)
		super(QtGui.QGraphicsView, self).__init__(self.scene, parent)

		self.scene.setSceneRect(0, 0,
				self.width + 2 * self.edge,
				self.height + 2 * self.edge)

	def set_game(self, game):
		self.game = game

	def go_next(self):
		prev = self.game.where()
		try:
			self.game.forth()
		except sgf.SGFNoMoreNode:
			print "End of game or branch."
			return
		print "GUI: %s" % (self.game.where())
		self.handle_node(prev, self.game.where())

	def go_prev(self):
		prev = self.game.where()
		if not prev.prop == "":
			x, y = util.pos2xy(self.game.where().prop)
			self.remove_stone(x, y)
			super(GoBoard, self).remove_stones([(x, y)])
		try:
			self.game.back()
			self.handle_node(prev, self.game.where(), True)
		except sgf.SGFNoMoreNode:
			pass

	def attach_undo(self, node, added, removed):
		def _undo():
			print "_undo %s" % node
			for x, y in added:
				self.remove_stone(x, y)
			for x, y in removed:
				cl = util.str2color(node.name)
				self.add_stone(x, y, util.enemy(cl))
				self.place_stone_xy(x, y, util.enemy(cl))
		return _undo

	def handle_node(self, prev, node, back=0):
		"Handle a node, like mark, comment, etc. dead stone is not handled here"
		self.emit(QtCore.SIGNAL("newComment(PyQt_PyObject)"), "")
		self.clear_marks()
		added = []
		removed = []

		if node.is_root():
			return

		if back:
			try:
				node.undo()
			except AttributeError:
				pass  # Allow node with no undo

		if util.is_stone(node.name):
			added.extend(self.handle_stone(node))
		# When going back, the stone is already there
		elif util.is_move(node.name):
			if not back:
				removed.extend(self.handle_move(node))
			if not node.prop == "":  # PASS
				self.refresh_cross(node)

		# Closure magic
		prev.undo = functools.partial(self.attach_undo, node, added, removed)()

		comment = ""
		for e in node.extra:
			print "Handling %s..." % e, node.extra[e]
			if util.is_comment(e):
				comment = node.get_comment()
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
		self.emit(QtCore.SIGNAL("newComment(PyQt_PyObject)"), comment)

	def clear_marks(self):
		"""Assuming that marks are only relavant for a particular move and ALL
		should be cleared from board"""
		while True:
			try:
				self.scene.removeItem(self.marks.pop())
			except IndexError:
				break

	def refresh_cross(self, node):
		x, y = util.pos2xy(self.game.where().prop)
		cx, cy = self.convert_coord((x, y))
		cross = Cross(QtCore.QPointF(cx, cy), 10)
		cross.setZValue(10)
		self.scene.addItem(cross)
		self.marks.append(cross)

	def handle_move(self, node):
		"Handle a move. Deal with dead stone, etc. Assuming it's a play node"
		if node.prop == "":
			print "PASS"
			self.emit(QtCore.SIGNAL("newComment(PyQt_PyObject)"), "PASS")
			return []
		else:
			x, y = util.pos2xy(self.game.where().prop)
			return self.play_xy(x, y, util.str2color(self.game.where().name))

	def handle_stone(self, node):
		add = []
		for l in node.prop:
			print "Placing stone at %s" % l
			x, y = util.pos2xy(l)
			add.append((x, y))
			self.add_stone(x, y, util.str2color(node.name))

	def _handle_LB(self, labels):
		for l in labels:
			pos, char = l.split(":")
			x, y = util.pos2xy(pos)
			self.add_label(x, y, char)

	def _handle_CR(self, locs):
		for l in locs:
			x, y = util.pos2xy(l)
			self.add_circle(x, y, 10)

	def _handle_TR(self, locs):
		for l in locs:
			x, y = util.pos2xy(l)
			self.add_triangle(x, y, 10)

	def _handle_SQ(self, locs):
		for l in locs:
			x, y = util.pos2xy(l)
			self.add_square(x, y, 10)

	def _handle_MA(self, locs):
		for l in locs:
			x, y = util.pos2xy(l)
			self.add_mark(x, y, 2)

	def _remove_stones(self, group):
		remove = []
		for prop in group:
			x, y = util.pos2xy(prop)
			self.remove_stone(x, y)
			remove.append((x, y))
		super(GoBoard, self).remove_stones(remove)

	def go_up(self):
		"Go up in variantions"
		prev = self.game.where()
		remove = self.game.branch_up()
		if len(remove) == 0:
			return
		self._remove_stones(remove)
		self.handle_node(prev, self.game.where())

	def go_down(self):
		"Go up in variantions"
		prev = self.game.where()
		remove = self.game.branch_down()
		if len(remove) == 0:
			return
		self._remove_stones(remove)
		self.handle_node(prev, self.game.where())

	def mousePressEvent(self, event):
		if event.button() != QtCore.Qt.LeftButton:
			return
		self.go_next()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Right:
			self.go_next()
		elif event.key() == QtCore.Qt.Key_Left:
			self.go_prev()
		elif event.key() == QtCore.Qt.Key_Up:
			self.go_up()
		elif event.key() == QtCore.Qt.Key_Down:
			self.go_down()

	def mouseReleaseEvent(self, event):
		pass
		# print "mouse released ", event.button(), event.pos()

	def out_of_board(self, pix):
		x, y = pix
		if x < self.x0 or y < self.y0 or x > self.x1 or y > self.y1:
			return True
		else:
			return False

	def convert_pixel_coord(self, pix):
		if self.out_of_board(pix):
			return (-1, -1)

		px, py = pix
		px -= self.edge
		py -= self.edge
		return ((px + self.w / 2) / self.w + 1, (py + self.h / 2) / self.h + 1)

	def convert_coord(self, go):
		"convert stone logical position into pixel postion"
		gx, gy = go
		if gx > 19 or gy > 19 or gx < 0 or gy < 0:
			return (-1, -1)

		return ((gx - 1) * self.w + self.edge,
				(gy - 1) * self.w + self.edge)

	def draw_stars(self):
		stars = [(4, 4), (4, 10), (4, 16), (10, 4), (10, 16),
			(16, 4), (16, 10), (16, 16), (10, 10)]
		for x, y in stars:
			sx, sy = self.convert_coord((x, y))
			sx -= 5
			sy -= 5
			self.scene.addEllipse(sx, sy, 10, 10, brush=QtGui.QBrush(QtCore.Qt.black))

	def draw_board(self):
		pen = QtGui.QPen()
		pen.setWidth(2)

		# Draw background
		bg_color = QtGui.QColor(0xcb, 0x91, 0x43)
		self.scene.setBackgroundBrush(QtGui.QBrush(bg_color))
		# self.scene.addPixmap(QPixmap("res/wood.jpg"))

		self.draw_stars()

		# Draw frame
		rect = QtCore.QRectF(self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0)
		self.scene.addRect(rect, pen)

		# Draw lines
		for i in range(18):
			x = self.x0 + i * self.w
			y = self.y0 + i * self.h
			line = QtGui.QGraphicsLineItem()
			line.setLine(x, self.y0, x, self.y1)
			self.scene.addItem(line)

		for i in range(18):
			x = self.x0 + i * self.w
			y = self.y0 + i * self.h
			line = QtGui.QGraphicsLineItem()
			line.setLine(self.x0, y, self.x1, y)
			self.scene.addItem(line)

		self.setRenderHint(QtGui.QPainter.Antialiasing)
		self.show()

	def add_stone(self, x, y, color):
		""" Doesn't change model """
		stone = Stone(color)
		gi = QtGui.QGraphicsPixmapItem(stone.get_bitmap())
		self.stones[x - 1][y - 1] = gi
		x, y = self.convert_coord((x, y))
		x -= 0.5 * self.w  # FIXME: somehow, this is in the middle
		y -= 0.5 * self.w
		gi.setPos(x, y)

		effect = QtGui.QGraphicsDropShadowEffect(self)
		effect.setBlurRadius(1)
		effect.setOffset(3.0)
		gi.setGraphicsEffect(effect)

		self.scene.addItem(gi)

		return gi

	def add_label(self, x, y, char):
		""" Doesn't change model """
		font = QtGui.QFont()
		font.setPixelSize(20)

		tx = QtGui.QGraphicsTextItem()
		tx.setPlainText(char)
		tx.setDefaultTextColor(QColor("yellow"))
		tx.setFont(font)
		self.scene.addItem(tx)
		self.marks.append(tx)  # overwriting previous one. should be GCed
		x, y = self.convert_coord((x, y))
		x -= 10
		y -= 20
		tx.setPos(x, y)
		tx.setZValue(5)

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
		gi = self.stones[x - 1][y - 1]
		self.scene.removeItem(gi)

	def play_xy(self, x, y, color):
		try:
			dead = super(GoBoard, self).play_xy(x, y, color)
			# Add only as the model knows about this new stone
			self.add_stone(x, y, color)
			for dx, dy in dead:
				self.remove_stone(dx, dy)
			return dead
		except IndexError:
			print "Unable to make move: (%d,%d,%d)" % (x, y, color)
			# Remove the just played stone
			pass

	def _clear(self):
		# TODO: remove existing stones
		# TODO: might need a modified flag
		# print "GoBoard: number of stones on board: ", len( self.stones_gi )

		# Clearing all current stuff TODO: refresh the board instead.
		# set_trace()
		# for gi in self.scene.items():
			# self.scene.removeItem(gi)

		self.draw_board()

	def setup(self):
		self.clear()


class MyWidget(QtGui.QWidget):
	def __init__(self, fn, parent=None):
		super(MyWidget, self).__init__(parent)

		self.goban = GoBoard(self)
		self.goban.draw_board()

		try:
			ad = adapter.getAdapter(fn)
			self.game = sgf.Game(ad.adapt())
		except adapter.AdapterError as e:
			print "Adapter: %s" % e
		except IOError:
			print "Unable to get adapter"

		self.game.build_tree()

		self.goban.set_game(self.game)
		self.goban.setup()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.goban)
		self.setLayout(layout)


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.createActions()
		self.createMenus()
		self.setWindowTitle("WQ")
		self.setWindowIcon(QtGui.QIcon(':res/icon320x320.png'))

		if len(sys.argv) > 1:
			self.widget = MyWidget(sys.argv[1])
			self.setCentralWidget(self.widget)
			self.createDockWindows()
			self.resize(1200, 900)
		else:
			self.resize(200, 200)

	def open(self):
		fn = QtGui.QFileDialog.getOpenFileName(caption="Open File",
			filter="(*.sgf *.gib)")
		self.widget = MyWidget(str(fn))
		self.setCentralWidget(self.widget)
		self.createDockWindows()
		self.resize(1200, 900)
		self.widget.setFocus()

	def next(self):
		print 'Move to next'
		self.widget.next()

	def reset(self):
		print 'Reset'
		self.widget.goban.clear()

	def about(self):
		QtGui.QMessageBox.about(self, "WQ",
				"Cross platform weiqi game replayer.")

	def aboutQt(self):
		print "Invoked <b>Help|About Qt</b>"

	def createActions(self):
		self.openAct = QtGui.QAction("&Open...", self,
				shortcut=QtGui.QKeySequence.Open,
				statusTip="Open an existing file", triggered=self.open)

		self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
				statusTip="Exit the application", triggered=self.close)

		self.aboutAct = QtGui.QAction("&About", self,
				statusTip="Show the application's About box",
				triggered=self.about)

		self.aboutQtAct = QtGui.QAction("About &Qt", self,
				statusTip="Show the Qt library's About box",
				triggered=self.aboutQt)
		self.aboutQtAct.triggered.connect(QtGui.qApp.aboutQt)

	def createMenus(self):
		self.fileMenu = self.menuBar().addMenu("&File")
		self.fileMenu.addAction(self.openAct)
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
		dock = QtGui.QDockWidget("Game Info", self)
		dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea |
			QtCore.Qt.RightDockWidgetArea)
		self.gameInfoEdit = QtGui.QTextEdit()
		self.gameInfoEdit.setReadOnly(True)
		self.gameInfoEdit.setFixedHeight(100)
		dock.setWidget(self.gameInfoEdit)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
		self.populateGameInfo()

		dock = QtGui.QDockWidget("Comment", self)
		self.commentEdit = QtGui.QTextEdit()
		self.commentEdit.setReadOnly(True)
		dock.setWidget(self.commentEdit)
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)

		self.connect(self.widget.goban, QtCore.SIGNAL("newComment(PyQt_PyObject)"),
			self.displayComment)


# MAIN MAIN MAIN ######################################
def main():
	app = QtGui.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

# Eof
