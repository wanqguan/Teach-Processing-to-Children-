class FlowField :
    def __init__(self, r) :
        self.resolution = r
        # Determine the number of columns and rows based on sketch's width and height
        self.cols = 640/r  # Attention
        self.rows = 360/r
        self.field = []
        self.init()

    def init(self):
        # Reseed noise so we get a new flow field every time
        noiseSeed(int(random(10000)))
        self.field = []
        xoff = 0
        for i in range(self.cols):
            yoff = 0
            tmp = []
            for j in range(self.rows):
                theta = map(noise(xoff,yoff),0,1,0,TWO_PI)
                # Polar to cartesian coordinate transformation to get x and y components of the vector
                tmp.append(PVector(cos(theta),sin(theta)))
                yoff += 0.1
            self.field.append(tmp)
            xoff += 0.1

    def display(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.drawVector(self.field[i][j],i*self.resolution,j*self.resolution,self.resolution-2)


    def drawVector(self, v, x, y, scayl) :
        pushMatrix()
        arrowsize = 4
        # Translate to location to render vector
        translate(x,y)
        stroke(0,100)
        # Call vector heading function to get direction (note that pointing up is a heading of 0) and rotate
        rotate(v.heading2D())
        # Calculate length of vector & scale it to be bigger or smaller if necessary
        len = v.mag()*scayl
        # Draw three lines to make an arrow (draw pointing up since we've rotate to the proper direction)
        line(0,0,len,0)
        #line(len,0,len-arrowsize,+arrowsize/2)
        #line(len,0,len-arrowsize,-arrowsize/2)
        popMatrix()
    
    
    def lookup(self, lookup) :
        column = int(constrain(lookup.x/self.resolution,0,self.cols-1))
        row = int(constrain(lookup.y/self.resolution,0,self.rows-1))
        return self.field[column][row].get()
  
