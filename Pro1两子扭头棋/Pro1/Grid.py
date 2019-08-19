class Grid():
    
    
    def __init__(self, xn, yn, xl, yl):
        self.xn = xn # n of grids
        self.yn = yn
        self.xl = xl # one grid's len
        self.yl = yl
        self.xll = xl * xn
        self.yll = yl * yn
        
    def draw(self):
        stroke(200) 
        for xi in range(self.xn+1):
            line(xi * self.xl, 0, xi * self.xl, self.xll)
        for yi in range(self.yn+1):
            line(0, yi * self.yl, self.yll, yi * self.yl)
        
