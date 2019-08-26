from Boxes import Boxes
from Board import Board

an = 5
bn = 4

board = Board()
boxes = Boxes(an, bn, 60, 60, 30, 30, board)



def setup():
    size(600, 600, P2D)
    colorMode(HSB, 100)
    background(30)
    boxes.draw()
    
def draw():
    clear()
    background(30)
    boxes.draw()
    board.draw()
    
def mouseClicked():
    boxes.parse_button(mouseX, mouseY)
    
def keyPressed():
    "reset"
    global board, boxes
    board = Board()
    boxes = Boxes(an, bn, 60, 60, 30, 30, board)
