add_library('geomerative')
add_library('fisica')

from random import random
from copy import deepcopy


def setup():
    global grp, world, lines
    size(1500,800)
    
    
    RG.init(this)
    grp = RG.getText("50", "FreeSans.ttf",600, CENTER)
    
    Fisica.init(this)
    world = FWorld()
    
    lines = []
    for i in range(2):
        points = grp.children[i].getPoints()
        for p2, p1 in zip(points[:-1], points[1:]):
            my_line = FLine(p1.x+width/2, p1.y+height/1.5, 
                            p2.x+width/2, p2.y+height/1.5)
            my_line.setStatic(False)
            lines.append(my_line)
            world.add(my_line)

    
def draw():
    background(255, 10)
    #grp.draw()
    world.draw()
    world.step()
    
    if mousePressed and frameCount%10==0:
        global ball_img
        s = 10+random()*30
        ball = FCircle(s*1.5)
        ball.setPosition(mouseX, mouseY)
        
        ball_img = loadImage("mid1.png")
        ball_img.resize(int(s), int(s))
        ball.attachImage(ball_img)
        del ball_img
        world.add(ball)
    
def keyPressed():
    if key == 'v':
        for l in lines:
            l.setDrawable(not l.isDrawable())
