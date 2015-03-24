#!/usr/bin/python

import sys
import os
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pdb

from collection import Collection

#TODO:
# once the board is resize, everything is in a mess
# needs a bit of edge for the board.
# Stop hard-coding stone size, etc.
# Draw star, tianyuan, etc

from sgfparser import *

class EnhancedCursor(Cursor):
    """ Adds the following features to Cursor in sgfparser.py: 
        - comments from the SGF file in the current node are automatically displayed
          in the ScrolledText widget self.comments 
        - It remembers if it is in a 'wrong variation', and correctChildren returns a list
          of the correct children variations. """

    def __init__(self, sgf):
        self.wrongVariation = 0
        Cursor.__init__(self, sgf, 1)

    def correctChildren(self):
        if self.wrongVariation:
            return []
        
        corr = []
        n = self.currentN.next
        i = 0
        
        while n:
            c = n.getData()
            if not (c.has_key('TR') or c.has_key('WV')):
                corr.append(i)
            n = n.down
            i += 1
        return corr

    def reset(self):
        self.game(0)
        self.wrongVariation = 0

    def next(self, varnum=0):
        n = Cursor.next(self, varnum)
        if not self.wrongVariation and (n.has_key('TR') or n.has_key('WV')): self.wrongVariation = 1
        elif self.wrongVariation:
            self.wrongVariation = self.wrongVariation + 1
        print "next: ", n
        return n

    def previous(self):
        n = Cursor.previous(self)
        if self.wrongVariation:
            self.wrongVariation = self.wrongVariation - 1
        print "previous", n
        return n

BLACK_STONE = 'B'
WHITE_STONE = 'W'

class Bitmap:
    @staticmethod
    def get_bitmap_for_stone(color):
        if ( color == BLACK_STONE ):
            return "res/yun_b.png"
        else:
            return "res/yun_w.png"

    @staticmethod
    def get_bg_bitmap():
        return "background.png"

class Stone:
    def __init__(self,color):
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


class abstractBoard:
    """ This class administrates a go board.
        It keeps track of the stones currently on the board in the dictionary self.status,
        and of the moves played so far in self.undostack

        It has methods to clear the board, play a stone, undo a move. """

    def __init__(self, boardSize = 19):
        self.status = {}
        self.undostack = []
        self.boardSize = boardSize

    def neighbors(self,x):
        """ Returns the coordinates of the 4 (resp. 3 resp. 2 at the side / in the corner) intersections
            adjacent to the given one. """
        if   x[0]== 1              :     l0 = [2]
        elif x[0]== self.boardSize :     l0 = [self.boardSize-1]
        else:                            l0 = [x[0]-1, x[0]+1]

        if   x[1]== 1              :     l1 = [2]
        elif x[1]== self.boardSize :     l1 = [self.boardSize-1]
        else:                            l1 = [x[1]-1, x[1]+1]

        l = []
        for i in l0: l.append((i,x[1]))
        for j in l1: l.append((x[0],j))

        return l

    def clear(self):
        """ Clear the board """
        self.status = {}
        self.undostack=[]        

    def play(self,pos,color):
        """ This plays a color=black/white stone at pos, if that is a legal move
            (disregarding ko), and deletes stones captured by that move.
            It returns 1 if the move has been played, 0 if not. """

        if self.status.has_key(pos):                # check if empty
            return 0

        l = self.legal(pos,color)
        if l:                                       # legal move?
            captures = l[1]
            for x in captures: del self.status[x]   # remove captured stones, if any
            self.undostack.append((pos,color,captures))   # remember move + captured stones for easy undo
            return 1
        else: return 0

    def legal(self, pos, color):
        """ Check if a play by color at pos would be a legal move. """
        c = [] # captured stones
        for x in self.neighbors(pos):
            if self.status.has_key(x) and self.status[x]==self.invert(color):
                c = c + self.hasNoLibExcP(x, pos)        

        self.status[pos]=color

        if c:
            captures = []
            for x in c:
                if not x in captures: captures.append(x)
            return (1, captures)

        if self.hasNoLibExcP(pos):
            del self.status[pos]
            return 0
        else: return (1, [])

    def hasNoLibExcP(self, pos, exc = None):
        """ This function checks if the string (=solidly connected) of stones containing
            the stone at pos has a liberty (resp. has a liberty besides that at exc).
            If no liberties are found, a list of all stones in the string is returned.

            The algorithm is a non-recursive  implementation of a simple flood-filling:
            starting from the stone at pos, the main while-loop looks at the intersections
            directly adjacent to the stones found so far, for liberties or other stones that belong
            to the string. Then it looks at the neighbors of those newly found stones, and so
            on, until it finds a liberty, or until it doesn't find any new stones belonging
            to the string, which means that there are no liberties.
            Once a liberty is found, the function returns immediately. """
            
        st = []            # in the end, this list will contain all stones solidly connected to the
                           # one at pos, if this string has no liberties
        newlyFound = [pos] # in the while loop, we will look at the neighbors of stones in newlyFound
        foundNew = 1
        
        while foundNew:
            foundNew = 0
            n = []         # this will contain the stones found in this iteration of the loop
            for x in newlyFound:
                for y in self.neighbors(x):
                    if not self.status.has_key(y) and y != exc:    # found a liberty
                        return []
                    elif self.status.has_key(y) and self.status[y]==self.status[x] \
                         and not y in st and not y in newlyFound: # found another stone of same color
                        n.append(y)
                        foundNew = 1

            st[:0] = newlyFound
            newlyFound = n

        return st     # no liberties found, return list of all stones connected to the original one

    def undo(self, no=1):
        """ Undo the last no moves. """
        for i in range(no):
            if self.undostack:
                pos, color, captures = self.undostack.pop()
                del self.status[pos]
                for p in captures: self.status[p] = self.invert(color)

    def remove(self, pos):
        """ Remove a stone form the board, and store this action in undostack. """
        
        self.undostack.append(((-1,-1), self.invert(self.status[pos]), [pos]))
        del self.status[pos]

    def invert(self,color):
        if color == 'B': return 'W'
        else: return 'B'


class GoBoard(abstractBoard, QGraphicsView):
    def __init__(self, parent= None, size=19):
        abstractBoard.__init__(self, size)
        self.size=19
        self._stone_zvalue = 5
        self.w=20
        self.h=20
        self.edge = 25 
        self.x0 = 0 + self.edge
        self.y0 = 0 + self.edge
        self.width = (self.size-1)*self.w
        self.height = (self.size-1)*self.h
        self.x1 = (self.size-1)*self.w + self.edge
        self.y1 = (self.size-1)*self.h + self.edge

        self.scene = QGraphicsScene( 0, 0, 
                                    self.width + 2 * self.edge,
                                    self.height + 2 * self.edge )
        super(QGraphicsView, self).__init__(self.scene, parent)

        self.setSceneRect( 0, 0,
                          self.width + 2 * self.edge,
                          self.height + 2 * self.edge )

        self.current_stone = BLACK_STONE
        self.cursor = None
        self.modified = False
        self.next_move = None
        self.stones = {}

    def next_stone(self):
        if self.current_stone == BLACK_STONE:
            self.current_stone = WHITE_STONE
        else:
            self.current_stone = BLACK_STONE

    def get_possible_move(self, pos):
        """ get next possible move at pos, returning null if none found. this is
        used for handling mouse click"""
        x, y = pos
        for i in range(self.cursor.noChildren()):
            c = self.cursor.next(i) # try i-th variation
            print "child ", c, " c[current_stone] ", c[self.current_stone][0]
            if c.has_key( self.current_stone ) and self._at2digit(c[self.current_stone][0]) == (x,y):
                print "get_possible_move: Found move"
                return c
        return None

    def _reply_move(self):
        try:
            self.next_move = self.cursor.next()
            self.handle_sgf_node( self.next_move )
        except SGFError:
            print "_reply_move: can't find reply, something wrong with sgf?"
            return

    def mousePressEvent(self, event):
        # TODO handle stat
        # TODO: should really move these to mouseUp event
        #print "mouse button pressed at ", event.button(), event.pos()
        x, y = self.convert_pixel_coord( (event.pos().x(), event.pos().y()) )
        #print "Placing stone at %d, %d" % (x,y)
        if x == -1 or y == -1:
            return

        try:
            # look for the move in the SGF file
            move = self.get_possible_move( (x,y) )
            if move:
                # Play the stone in the right way
                self.handle_sgf_node( move )
                self.next_stone()
                self._reply_move()
                self.next_stone()
                # Handle right or wrong
                if self.cursor.wrongVariation == 1:        # just entered wrong variation
                    print 'WRONG!!!'
                else:
                    print 'CORRECT!!!'
            else:
                # Need to rewind the cursor here as it was advanced by
                # get_possible_move()
                self.cursor.previous()
                print 'mousePressEvent: wrong path'
        except SGFError:
           self.cursor.previous()
           print 'SGF error'
           return

    def mouseReleaseEvent(self, event):
        print "mouse released ", event.button(), event.pos()

    def out_of_board(self, pix):
        x,y = pix
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

        return ( (gx-1)*self.w- Stone.get_width()/2 + self.edge, 
                ((gy-1)*self.w- Stone.get_width()/2)  + self.edge )
    
    def draw_stars(self):
        stars = [ (4,4), (4,16), (16,4), (16,16), (10,10) ]
        for s in stars:
            x, y = (s[0]*self.w, s[1]*self.h)
            self.scene.addEllipse( x, y, 2, 2 )

    def draw_board(self):
        pen = QPen()
        pen.setWidth(2)

        # Draw background 
        bg_color = QColor( 0xcb, 0x91, 0x43 )
        self.scene.setBackgroundBrush( QBrush(bg_color) )

        #self.draw_stars()

        # Draw frame
        rect = QRectF( self.x0, self.y0, self.x1 - self.x0,  self.y1 - self.y0 )
        self.scene.addRect( rect, pen  )

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

    def is_valid_pos(self, pos):
        x,y = pos
        if ( x < 1 or x > 19 or y < 1 or y > 19 ):
            return False
        else:
            return True

    def play_stone(self, color, pos):
        # will have to see if it's leagal or not
        # The following are borrowed from the original board1.py
        if abstractBoard.play(self, pos, color):                    # legal move?
            captures = self.undostack[len(self.undostack)-1][2]     # retrieve list of captured stones
            print "captures: ", captures
            for x in captures:
                self.remove_stone( x )
            self.place_stone( color, pos )
        self.modified = True

    def place_stone(self, color, pos):
        # Note: Should never be called directly!!!
        if not self.is_valid_pos(pos):
            return None

        stone = Stone(color)
        gi = self.scene.addPixmap( stone.get_bitmap() )
        gi.setZValue( self._stone_zvalue )
        x, y = self.convert_coord( pos )
        gi.setPos( x, y )
        return gi


    def _digit2at(self, pos):
        "Convert position in digit format to AT format"
        at="ABCDEFGHIJKLMNOPQRST"
        digit=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
        str = ""
        x,y = pos
        str += at[digit.index(x)]
        str += at[digit.index(y)]

        return str
    
    def _at2digit(self, pos):
        """Convert position in AT format into digit format"""
        at="ABCDEFGHIJKLMNOPQRST"
        digit=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
        x = pos[0].upper()
        y = pos[1].upper()

        xx = digit[at.index(x)]
        yy = digit[at.index(y)]

        return (xx, yy)

    def place_stone_AT(self, color, pos):
        xx, yy = self._at2digit( pos )

        #print "place_stone_AT ", pos
        s = self.place_stone( color, (xx,yy))
        if s:
            self.stones[pos.upper()] = s
        abstractBoard.play( self, (xx,yy), color )

    def remove_stone(self, pos):
        #print "remove_stone: removing ", item
        print "remove_stone: pos ", self._digit2at(pos)
        gi = self.stones.pop( self._digit2at(pos) )
        self.scene.removeItem( gi )

    def delShadedStone(self):
        print "delShadedStone() stubbed"

    def play(self, pos, color=None):
        """ Play a stone of color (default is self.currentColor) at pos. """

        if color is None: color = self.currentColor
        if abstractBoard.play(self, pos, color):                    # legal move?
            captures = self.undostack[len(self.undostack)-1][2]     # retrieve list of captured stones
            print "captures: ", captures
            for x in captures:
                self.remove_stone( self.stone[x] )
            self.place_stone(pos, color)
            self.currentColor = self.invert(color)
            self.delShadedStone()
            return 1
        else: return 0

    def set_cursor(self, cursor):
        self.cursor = cursor;

    def _is_setup_node(self, node):
        """ decide if a sgf node is for setup or game play"""
        dict = [ 'B', 'W' ]
        for k in node.keys():
            if k in dict:
                return False

        return True

    def clear(self):
        #TODO: remove existing stones
        #TODO: might need a modified flag
        #print "GoBoard: number of stones on board: ", len( self.stones_gi )
        #for s in self.stones_gi:
            #self.scene.removeItem( s )
        for k in self.stones.keys():
            self.stones.pop( k )
        
        # Clearing all current stuff TODO: refresh the board instead.
        for i in self.scene.items():
            self.scene.removeItem( i )

        self.draw_board()

        abstractBoard.clear(self)


    def reset_cursor(self):
        self.cursor.game(0)

    def _find_play_move(self, node):
        "for a node, find the part that is a play mark"
        for k in node.keys():
            if k == 'B' or k == 'W':
                return k

        return None

    def setup(self):
        self.clear()
        print "abstractBoard::status ", self.status

        self.reset_cursor()
        self.next_move = self.cursor.currentNode()
        try:
            while self._is_setup_node( self.next_move ):
                self.handle_sgf_node( self.next_move )
                self.next_move = self.cursor.next()

            # Start of game play
            # FIXME Handle where _find_play_move() returns None
            self.current_stone = self._find_play_move( self.next_move )
            print "%s FIRST." % self.current_stone
            self.cursor.previous() # un-wind
        except SGFError:
            print "Probably end of variation"

        self.modified = False

    def do_AB(self, list):
        for i in list:
            self.place_stone_AT( BLACK_STONE, i )

    def do_AW(self, list):
        for i in list:
            self.place_stone_AT( WHITE_STONE, i )

    def do_play_node(self, color, pos):
        "color: 'B' or 'W'; pos: AT position of a stone"
        print "do_play_node: ", color, pos
        x,y = self._at2digit( pos )
        if abstractBoard.play(self, (x,y), color):                    # legal move?
            captures = self.undostack[len(self.undostack)-1][2]     # retrieve list of captured stones
            print "captures: ", captures
            for c in captures:
                self.remove_stone( c )
            self.place_stone_AT( color, pos )

    def handle_sgf_node(self, node):
        " Blindly handles all node. It's the caller's job for state checking."
        # TODO: needs to add more node type, comment handling, etc
        self.modified = True
        for k in node.keys():
            print 'handle_sgf_node: node: ', node
            if k == 'AB':
                self.do_AB( node['AB'] )
            elif k == 'AW':
                self.do_AW( node['AW'] )
            elif k == 'B':
                self.do_play_node( 'B', node['B'][0] )
            elif k == 'W':
                self.do_play_node( 'W', node['W'][0] )
            else:
                ret = 0
                print "Don't know what to do yet."

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self ).__init__(parent)
        self.goban = GoBoard(self)
        self.goban.draw_board()
        self.coll = Collection( sys.argv[1] )
        sgf = EnhancedCursor( self.coll.get_next() )

        self.goban.set_cursor( sgf )
        self.goban.setup()

    def next(self):
        if self.coll is None:
            return

        found = False

        while not found:
            try:
                sgf = EnhancedCursor( self.coll.get_next() )
                self.goban.set_cursor( sgf )
                self.goban.setup()
                found = True
                #TODO: need to handle running ouf of problems.
            except SGFError:
                print "SGF error"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widget = MyWidget()
        self.setCentralWidget(self.widget)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("WQ")

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

