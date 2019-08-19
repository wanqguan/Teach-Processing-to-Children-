class Man():
    
    
    def __init__(self, xl, yl, px, py, pxmax, pymax, dir= 0.0, big= 20, name = ''):
        self.p = PVector(px, py)
        self.xl= xl  # x axis single grid's len
        self.yl = yl  # y axis single grid's len
        self.dir = PVector.fromAngle(0)  # set direction
        self.big = big  # the display size of the man
        self.name = name  # 'a' or 'b'
        self.pxmax = pxmax
        self.pymax = pymax

    def move(self, tmp):
        if PVector.angleBetween(self.dir, tmp)< 0.1:
            ans = self.p + tmp
            if 0<= ans.x < self.pxmax and 0<= ans.y < self.pymax:  # if the new place of the man not beyond the screen
                self.p = ans
        else:
            self.dir = tmp.copy()
                
    def draw(self):
        
        rectMode(CENTER)
        if self.name == 'a':
            fill(300, 0, 0) # choose the fill color(RGB)
        else:
            fill(100, 200, 0)
        rect((self.p.x+0.5) * self.xl, (self.p.y+0.5) * self.yl, self.big, self.big)
        tmp = PVector.add(self.p, self.dir*0.2)
        fill(0, 0, 300)
        rect((tmp.x+0.5) * self.xl, (tmp.y+0.5) * self.yl, self.big*0.6, self.big*0.6)
        fill(200)
        textSize(40)
        text(self.name, (self.p.x+0.5) * self.xl, (self.p.y+0.5) * self.yl)
