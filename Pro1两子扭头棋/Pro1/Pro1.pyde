from Grid import Grid
from Man import Man
from Manager import Manager
from Board import Board

# init
grid = Grid(10, 10, 60, 60)
man1 = Man(60, 60, 5, 3, 10, 10, name='a')
man2 = Man(60, 60, 6, 6, 10, 10, name='b', dir = PI/2)
board = Board()
manager = Manager(man1, man2, board)

    
def restart():
    global man1, man2, manager, board
    man1 = Man(60, 60, int(random(0, 5)), int(random(9)), 10, 10, name='a')
    man2 = Man(60, 60, int(random(5, 9)), int(random(9)), 10, 10, name='b', dir = PI/2)
    #board = Board()
    manager = Manager(man1, man2, board)
    

def setup():
    size(800, 600)
    print('please contorl with : ASDW, JKLI')
    clear()
    background(70, 100, 110)
    grid.draw()
    manager.draw()
    if manager.restart == True:
        restart()
    
def draw():
    pass
    
    
def keyPressed():
    manager.get(key)
    clear()
    background(70, 100, 110)
    grid.draw()
    manager.draw()
    if manager.restart == True:
        restart()
    
