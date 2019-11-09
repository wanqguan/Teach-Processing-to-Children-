add_library('handy')
add_library('ocd')
add_library('fisica')


from my_module import *


k_f = 1e3
max_f = 1e5
v_max = 1e3
planet_show_size = 20
planet_f_size = 30
planet_n = 200
planet_show_ball = False
planet_show_line = True
planet_list = set()

sun_size = 30
k_f_sun = 1e9
f_sun_max = 1e4
cam_dis = 8e2
merge_dis = 30

pos_vec = PVector(50, 0)


def setup():
    global world, cam, PG1, H
    #frameRate(16)
    smooth()
    fullScreen(P3D)
    background(255)
    
    PG1 = createGraphics(width, height, P3D)  
    cam = Camera(this, width/2, height/2, cam_dis, width/2, height/2, 0)
    
    H = HandyRenderer(this)
    H.setFillGap(1)
    H.setFillWeight(5)
  
    Fisica.init(this)
    world = FWorld()
    world.setContactListener(ContactListener())
    world.setGravity(0, 0)
    

            
    sun = Sun(sun_size)
    sun.setStatic(True)
    sun.setName('sun')
    set_fbody(sun, pos=(width/2, height/2), sensor=True, fill=(250, 100, 100), stroke=-1)
    world.add(sun)
       

    
    
def draw():
    
    if frameCount < planet_n:
        p = Planet(planet_f_size)
        pos_vec = PVector(200, 0).rotate(PI*random(0.3, 1.8))
        v_vec = PVector.random2D().setMag(v_max)
        set_fbody(p, v=(v_vec.x, v_vec.y),
                  pos=(width/2+pos_vec.x, height/2+pos_vec.y), damp=-1, sensor=True, 
                  fill=(random(255), random(255), random(255)))
        world.add(p)
        planet_list.add(p)
        
    cam.feed()
    
    PG1.beginDraw()
    PG1.background(255, 50)
    PG1.stroke(0)
    PG1.text(width/2, height/2, len(planet_list))

    world.draw(PG1)
    PG1.endDraw()
    
    world.step()
    
    tint(255)
    image(PG1, 0, 0)
    if frameCount % 10:
        print(len(planet_list))
    


       
class ContactListener(FContactAdapter):

    def __init__(self):
        pass

    def contactPersisted(self, c):
        b1, b2 = c.getBody1(), c.getBody2()
        b1_p = PVector(b1.getX(), b1.getY())
        b2_p = PVector(b2.getX(), b2.getY())
        d = b1_p.sub(b2_p).copy()
        dm = d.magSq()
        if dm < merge_dis:
            world.remove(b2)
            planet_list.remove(b2)
        else:
            d1 = d.normalize().mult(-k_f/dm)
            d1.limit(max_f)
            d2 = d1.copy().mult(-1)
            # print(b1_p)
            b1.addForce(d1.x, d1.y)
            b2.addForce(d2.x, d2.y)
       
class Sun(FCircle):
    
    def draw(self, applet):
        fill(self.getFillColor())
        noStroke()
        H.ellipse(self.getX(), self.getY(), 
                                      sun_size, sun_size)
        
class Planet(FCircle):
    
    def draw(self, applet):
        self.mx = self.getX()
        self.my = self.getY()
        fill(self.getFillColor())
        
        pos = PVector(self.getX()-width/2, self.getY()-height/2)
        if pos.mag() < sun_size/2*1.1 or pos.mag()>500:
            world.remove(self)
            planet_list.remove(self)
        else:
            dm = pos.magSq()
            d1 = pos.normalize().mult(-k_f_sun/dm)
            d1.limit(f_sun_max)
            self.addForce(d1.x, d1.y)
            
        
        noStroke()
        if planet_show_ball: H.ellipse(self.getX(), self.getY(), 
                                      planet_show_size, planet_show_size)
        stroke(self.getFillColor())
        if hasattr(self, 'xb') and planet_show_line:
            H.line(self.xb, self.yb, self.mx, self.my)
        self.xb = self.mx
        self.yb = self.my
    
