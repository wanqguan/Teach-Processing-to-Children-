add_library('geomerative')
add_library('fisica')


from itertools import chain, cycle
from time import sleep
from random import random

files = [['name1', 'name2']]
fn = 0

ground_fric = 0

def set_fbody(fbody, pos=None, v=None, dens=None, damp=None, 
                  rest=None, fric=None, stroke=None, fill=None, img=None):
    if pos:
        fbody.setPosition(*pos)
    if v:
        fbody.setVelocity(*v)
    if dens:
        fbody.setDensity(dens)
    if damp:
        fbody.setDamping(damp)
    if rest:
        fbody.setRestitution(rest)
    if fric:
        fbody.setFriction(fric)
    if stroke:
        fbody.setStroke(*stroke)
    if fill:
        fbody.setFill(*fill)
    if img:
        fbody.attachImage(img)

def setup():
    global shp, points 
    global world
    # Initilaize the sketch
    size(1500,800)
    RG.init(this)
    
    RG.setPolygonizer(RG.UNIFORMLENGTH)
    RG.setPolygonizerLength(1)
    
    # Fisica
    Fisica.init(this)
    world = FWorld()
    
    ground = FLine(-width, height, width, height+20)
    set_fbody(ground, fric=ground_fric, rest=1)
    world.add(ground)
        
def draw():
    background(255)
    world.draw()
    world.step()
    world.setGravity(0.5e2, 1e2)

    if frameCount%3==0:
        s = 30+random()*30
        ball = FCircle(s)
        set_fbody(ball, pos=(20, height-20), v=(500, 500*random()), rest=1, fric=1, 
                  dens=1, fill=(255-s*2, 230, 230))
        ball.setNoStroke()
        world.add(ball)    
    
    
def keyPressed(): 
    global fn   
    
    if '1' <= key <= '9':
        k = int(key)
        img = loadImage('line' + str(k) + '.bmp')
        if not img:
            return
        x, y = img.width, img.height
        fb = FBox(x, y)
        set_fbody(fb, pos=(mouseX, mouseY), dens=0.05, rest=1, img = img)
        world.add(fb)
    elif key == ' ':
        names = files[fn] 
        fn = fn + 1 if fn != len(files)-1 else 0
                
        fc = FCompound()
        for ind, n in enumerate(names):
            n += '.svg'
            shp = RG.loadShape(n)
            shp = RG.centerIn(shp, g, 100)
            shp.setFill(1)
            
            points = shp.getPoints()
            for p in points:
                p.x /= 5
                p.y /= 5
                p.x += ind * 130
            points = points[1:-1:30]
        
    
            myPoly = FPoly()
            for p in points:
                myPoly.vertex(p.x+mouseX, p.y+mouseY)
            myPoly.setFill(245, 74, 177)
            fc.addBody(myPoly)
        world.add(fc)
    


        
