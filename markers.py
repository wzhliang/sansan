import math
from PyQt4 import QtCore
from PyQt4 import QtGui


class Cross(QtGui.QGraphicsItem):
	"Indicator of the current stone"
	Type = QtGui.QGraphicsItem.UserType + 2

	def __init__(self, point, size, mask):
		"point: QPointF object as I don't know the board"
		super(Cross, self).__init__()

		self.size = size
		self.point = point
		self.mask = mask
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

	def __init__(self, point, size, mask):
		"point: QPointF object as I don't know the board"
		super(Square, self).__init__()

		self.size = size
		self.point = point
		self.mask = mask
		self.topLeft = QtCore.QPointF(point.x() - size, point.y() - size)

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Square.Type

	def boundingRect(self):
		return QtCore.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		x1 = self.point.x() - self.size
		x2 = self.point.x() + self.size
		y1 = self.point.y() - self.size
		y2 = self.point.y() + self.size
		if self.mask:
			painter.drawPixmap(x1, y1, self.size * 2, self.size * 2, self.mask)

		line = QtCore.QLineF(x1, y1, x1, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(x1, y1, x2, y1)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(x2, y1, x2, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(x2, y2, x1, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)


class Triangle(QtGui.QGraphicsItem):
	"trangle mark"
	Type = QtGui.QGraphicsItem.UserType + 4

	def __init__(self, point, size, mask):
		"point: QPointF object as I don't know the board"
		super(Triangle, self).__init__()

		self.size = size
		self.point = point
		self.mask = mask

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Triangle.Type

	def boundingRect(self):
		return QtCore.QRectF(self.x() - self.size, self.y() - self.size,
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
		if self.mask:
			painter.drawPixmap(self.point.x() - self.size,
				self.point.y() - self.size,
				self.size * 2,
				self.size * 2,
				self.mask)

		line = QtCore.QLineF(x1, y1, x2, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(x2, y2, x3, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)

		line = QtCore.QLineF(x1, y1, x3, y2)
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawLine(line)


class Circle(QtGui.QGraphicsItem):
	"circle mark"
	Type = QtGui.QGraphicsItem.UserType + 5

	def __init__(self, point, size, mask):
		"point: QPointF object as I don't know the board"
		super(Circle, self).__init__()

		self.size = size
		self.point = point
		self.mask = mask

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QtCore.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		if self.mask:
			painter.drawPixmap(self.point.x() - self.size,
				self.point.y() - self.size,
				self.size * 2,
				self.size * 2,
				self.mask)
		# Draw the line itself.
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)


class Mark(QtGui.QGraphicsItem):
	"generic mark"
	Type = QtGui.QGraphicsItem.UserType + 6

	def __init__(self, point, size, mask):
		"point: QPointF object as I don't know the board"
		super(Mark, self).__init__()

		self.size = size
		self.point = point
		self.mask = mask

		self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
		# self.adjust() TODO: Do I need this?

	def x(self):
		return self.point.x()

	def y(self):
		return self.point.y()

	def type(self):
		return Circle.Type

	def boundingRect(self):
		return QtCore.QRectF(self.x() - self.size, self.y() - self.size,
			2.0 * self.size, 2.0 * self.size)

	def paint(self, painter, option, widget):
		if self.size <= 0:
			return

		# Draw the line itself.
		painter.setPen(QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine,
			QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
		painter.drawEllipse(self.point, self.size, self.size)
