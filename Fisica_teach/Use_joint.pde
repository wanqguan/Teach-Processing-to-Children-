add_library('fisica')


from my_module import *
from random import random


 
def setup():
    global world
    size(300, 300)
    Fisica.init(this)
    world = FWorld()
    world.setEdges()
    
    n = 10
    balls = []
    for i in range(n):
        x, y = sin(TWO_PI/n*i)*50+150, cos(TWO_PI/n*i)*50+150
        ball = FCircle(15)
        set_fbody(ball, pos=(x, y))
        world.add(ball)
        balls.append(ball)
        
    for i in range(len(balls)):
        for k in range(len(balls)):
            if i==k: continue
            joint = FDistanceJoint(balls[i], balls[k])
            joint.setFrequency(2)
            world.add(joint)
    
def draw():
    background(255)
    world.draw()
    world.step()
    
    





    
