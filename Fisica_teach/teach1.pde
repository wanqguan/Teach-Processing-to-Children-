add_library('fisica')


from my_module import *
from random import random

def contactStarted(c):
    print("hello")
    b1 = c.getBody1()
    b2 = c.getBody2()
    if not b1.isStatic() and b1.getSize()>1:
        b1.setSize(b1.getSize()*2)
    if not b2.isStatic() and b2.getSize()>1:
        b2.setSize(b2.getSize()*0.9)
 
def setup():
    global world
    size(300, 300)
    Fisica.init(this)
    world = FWorld()
    world.setEdges()
    
    ball = FCircle(20)
    set_fbody(ball, pos=(200, 200))
    world.add(ball)
    
    
def draw():
    background(255)
    world.draw()
    world.step()
    
    
def mousePressed():
    ball = FCircle(10 + 20*random())
    ball.setFilterBits(1)
    set_fbody(ball, pos=(mouseX, mouseY), v=(150-300*random(), 150-300*random()), 
              rest=1, fill = (255-100 * random(), 100, 100))
    world.add(ball)
    




    
